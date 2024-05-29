#include <Arduino.h>
#include <esp_camera.h>
#include <WiFi.h>
#include <AsyncUDP.h>

#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"

#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include "lwip/netdb.h"
#include "lwip/dns.h"

#include "quirc.h"

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// 4 for flash led or 33 for normal led
#define LED_GPIO_NUM       4

#define LED_LEDC_CHANNEL 2 //Using different ledc channel/timer than camera
#define CONFIG_LED_MAX_INTENSITY 255

#define QR_CODE_READER_STACK_SIZE 40 * 1024
#define QR_CODE_READER_TASK_PRIORITY 5

// const char* ssid     = "~Mk.";
// const char* password = "bs2z237u2k6pira";
const char* ssid     = "Mojo";
const char* password = "brilliancy";
int led_duty = 15;

const char *server_ip = "192.168.167.53";
uint16_t server_port = 5000;

WiFiClient client;

TaskHandle_t stream_handle;

void setupLedFlash(int pin);
// void connect_to_server();
void stream_feed(void *);

struct QRCodeReader
{
  TaskHandle_t qrcode_task_handler;
  framesize_t frameSize;
  camera_config_t camera_config;
  QueueHandle_t qrcode_queue;
  bool debug = true;
} qrcode_reader;

/* This structure holds the decoded QR-code data */
struct QRCodeData
{
  bool valid;
  int dataType;
  uint8_t payload[1024];
  int payloadLen;
};

void detect_qrcode(void *ctx);

void setup() {
  Serial.begin(115200);

  camera_config_t config;
  memset(&config, 0, sizeof(camera_config_t));

  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 10000000;
  config.frame_size = FRAMESIZE_QVGA;
  config.pixel_format = PIXFORMAT_JPEG; // for streaming
  //config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 15;
  config.fb_count = 1;
  
  Serial.print("Total heap: ");
  Serial.println(ESP.getHeapSize()); 
  Serial.print("Free heap: ");
  Serial.println(ESP.getFreeHeap()); 
  Serial.print("Total PSRAM: "); 
  Serial.println( ESP.getPsramSize());
  Serial.print("Free PSRAM: "); 
  Serial.println(ESP.getFreePsram());
  Serial.print("Has psram Enabled: ");
  Serial.println(psramFound());

   // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t *s = esp_camera_sensor_get();
  s->set_framesize(s, FRAMESIZE_QVGA);

  setupLedFlash(LED_GPIO_NUM);

  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  qrcode_reader.camera_config = config;

  xTaskCreatePinnedToCore(
    stream_feed,
    "stream-feed",
    4 * 1024,
    nullptr,
    2 /* uxPriority */,
    &stream_handle,
    1 /* xCoreID */
  );

  // xTaskCreatePinnedToCore(
  //   detect_qrcode, 
  //   "qrCodeDetectTask", 
  //   QR_CODE_READER_STACK_SIZE, 
  //   &qrcode_reader, 
  //   QR_CODE_READER_TASK_PRIORITY, 
  //   &qrcode_reader.qrcode_task_handler, 
  //   0  /* xCoreID */);
}

void loop() {
  vTaskDelay(1000);
}

void setupLedFlash(int pin) 
{
    ledcSetup(LED_LEDC_CHANNEL, 5000, 8);
    ledcAttachPin(pin, LED_LEDC_CHANNEL);
}

void enable_led(bool en)
{ // Turn LED On or Off
    int duty = en ? led_duty : 0;
    if (en && (led_duty > CONFIG_LED_MAX_INTENSITY))
    {
        duty = CONFIG_LED_MAX_INTENSITY;
    }
    ledcWrite(LED_LEDC_CHANNEL, duty);
}

void stream_feed(void *)
{
  Serial.print("[stream_feed] streaming feed...\n");
  camera_fb_t *fb = nullptr;
  size_t _jpg_buf_len = 0;
  uint8_t *_jpg_buf = nullptr;
  esp_err_t res = ESP_OK;

  enable_led(true);
  /*
  * // Perform an action every 10 ticks.
 * void vTaskFunction( void * pvParameters )
 * {
 * TickType_t xLastWakeTime;
 * const TickType_t xFrequency = 10;
 * BaseType_t xWasDelayed;
 *
 *     // Initialise the xLastWakeTime variable with the current time.
 *     xLastWakeTime = xTaskGetTickCount ();
 *     for( ;; )
 *     {
 *         // Wait for the next cycle.
 *         xWasDelayed = xTaskDelayUntil( &xLastWakeTime, xFrequency );
 *
 *         // Perform action here. xWasDelayed value can be used to determine
 *         // whether a deadline was missed if the code here took too long.
 *     }
 * }
  */
  const TickType_t xFrequency = 40;
  TickType_t xLastWakeTime = xTaskGetTickCount();
  BaseType_t xWasDelayed;
  while (true)
  {
    if(!client.connected()) {
      if(!client.connect(server_ip, server_port)) {
        // vTaskDelay(1000);    
        delay(2000);
        continue;
      }
    }    

    xWasDelayed = xTaskDelayUntil( &xLastWakeTime, xFrequency);
    // delay(400);

    fb = esp_camera_fb_get();
    if (!fb)
    {
      Serial.printf("Camera capture failed\n");
      res = ESP_FAIL;
    }
    else
    {
      if (fb->format != PIXFORMAT_JPEG)
      {
        bool jpeg_converted = frame2jpg(fb, 80, &_jpg_buf, &_jpg_buf_len);
        esp_camera_fb_return(fb);
        fb = nullptr;
        if (!jpeg_converted)
        {
            Serial.printf("JPEG compression failed!\n");
            res = ESP_FAIL;
        }
      }
      else
      {
          _jpg_buf_len = fb->len;
          _jpg_buf = fb->buf;
      }
    }

    if(res == ESP_OK) {
      client.write(_jpg_buf, _jpg_buf_len);
    }

    if (fb)
    {
        esp_camera_fb_return(fb);
        fb = nullptr;
        _jpg_buf = nullptr;
    }
    else if (_jpg_buf)
    {
        free(_jpg_buf);
        _jpg_buf = nullptr;
    }
    else if (res != ESP_OK)
    {
      Serial.printf("Frame failed!\n");
      break;
    }
  }
}

void dumpData(const struct quirc_data *data)
{
  Serial.printf("Version: %d\n", data->version);
  Serial.printf("ECC level: %c\n", "MLHQ"[data->ecc_level]);
  Serial.printf("Mask: %d\n", data->mask);
  Serial.printf("Length: %d\n", data->payload_len);
  Serial.printf("Payload: %s\n", data->payload);
}

void detect_qrcode(void *ctx)
{
  QRCodeReader *self = (QRCodeReader *)ctx;
  camera_config_t camera_config = self->camera_config;
  if (camera_config.frame_size > FRAMESIZE_SVGA)
  {
    if (self->debug)
    {
      Serial.println("Camera Size err");
    }
    vTaskDelete(nullptr);
    return;
  }

  struct quirc *q = nullptr;
  uint8_t *image = nullptr;
  camera_fb_t *fb = nullptr;

  uint16_t old_width = 0;
  uint16_t old_height = 0;

  if (self->debug)
  {
    Serial.printf("begin to qr_recognize\r\n");
  }
  q = quirc_new();
  if (q == nullptr)
  {
    if (self->debug)
    {
      Serial.print("can't create quirc object\r\n");
    }
    vTaskDelete(nullptr);
    return;
  }

  while (true)
  {
    if (self->debug)
    {
      Serial.printf("alloc qr heap: %u\r\n", xPortGetFreeHeapSize());
      Serial.printf("uxHighWaterMark = %d\r\n", uxTaskGetStackHighWaterMark(nullptr));
      Serial.print("begin camera get fb\r\n");
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);

    fb = esp_camera_fb_get();
    if (!fb)
    {
      if (self->debug)
      {
        Serial.println("Camera capture failed");
      }
      continue;
    }

    uint8_t *rgb_buf;
    // jpg2rgb888(fb->buf, fb->len, rgb_buf, JPG_SCALE_NONE);
    // rgb8882grayscale(rgb_buf, fb->width, fb->height);
    if (old_width != fb->width || old_height != fb->height)
    {
      if (self->debug)
      {
        Serial.printf("Recognizer size change w h len: %d, %d, %d \r\n", fb->width, fb->height, fb->len);
        Serial.println("Resize the QR-code recognizer.");
        // Resize the QR-code recognizer.
      }
      if (quirc_resize(q, fb->width, fb->height) < 0)
      {
        if (self->debug)
        {
          Serial.println("Resize the QR-code recognizer err (cannot allocate memory).");
        }
        esp_camera_fb_return(fb);
        fb = nullptr;
        image = nullptr;
        continue;
      }
      else
      {
        old_width = fb->width;
        old_height = fb->height;
      }
    }

    // Serial.printf("quirc_begin\r\n");
    image = quirc_begin(q, nullptr, nullptr);
    if (self->debug)
    {
      Serial.printf("Frame w h len: %d, %d, %d \r\n", fb->width, fb->height, fb->len);
    }
    memcpy(image, fb->buf, fb->len);
    quirc_end(q);

    if (self->debug)
    {
      Serial.printf("quirc_end\r\n");
    }
    int count = quirc_count(q);
    if (count == 0)
    {
      if (self->debug)
      {
        Serial.printf("Error: not a valid qrcode\n");
      }
      esp_camera_fb_return(fb);
      fb = nullptr;
      image = nullptr;
      continue;
    }

    for (int i = 0; i < count; i++)
    {
      struct quirc_code code;
      struct quirc_data data;
      quirc_decode_error_t err;

      quirc_extract(q, i, &code);
      err = quirc_decode(&code, &data);

      struct QRCodeData qrcode_data;

      if (err)
      {
        const char *error = quirc_strerror(err);
        int len = strlen(error);
        if (self->debug)
        {
          Serial.printf("Decoding FAILED: %s\n", error);
        }
        for (int i = 0; i < len; i++)
        {
          qrcode_data.payload[i] = error[i];
        }
        qrcode_data.valid = false;
        qrcode_data.payload[len] = '\0';
        qrcode_data.payloadLen = len;

        Serial.printf("Decoding FAILED: %s\n", error);
      }
      else
      {
        if (self->debug)
        {
          Serial.printf("Decoding successful:\n");
          dumpData(&data);
        }

        qrcode_data.dataType = data.data_type;
        for (int i = 0; i < data.payload_len; i++)
        {
          qrcode_data.payload[i] = data.payload[i];
        }
        qrcode_data.valid = true;
        qrcode_data.payload[data.payload_len] = '\0';
        qrcode_data.payloadLen = data.payload_len;
      }
      xQueueSend(self->qrcode_queue, &qrcode_data, (TickType_t)0);
      if (self->debug)
      {
        Serial.println();
      }
      Serial.printf("Decoding successful:\n");
      // dumpData(&data);
    }

    // Serial.printf("finish recoginize\r\n");
    esp_camera_fb_return(fb);
    fb = nullptr;
    image = nullptr;
  }
  quirc_destroy(q);
  vTaskDelete(nullptr);
}

void rgb8882grayscale(uint8_t *rgb, size_t len, uint8_t *gray) {
  
}