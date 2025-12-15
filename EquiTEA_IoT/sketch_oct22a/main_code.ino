#include <WiFi.h>
#include <HTTPClient.h>
#include "esp_camera.h"
#include "EquiTea_Image_Classification_inferencing.h"

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const char* serverBase = "http://YOUR_SERVER_IP:5000";
const char* recognizeRoute = "/recognize";

bool debug_nn = false;

String last_worker_id = "";
int last_weight = 0;

void setup() {
    Serial.begin(115200);

    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected");
    Serial.print("ESP32 IP address: ");
    Serial.println(WiFi.localIP());

    if (!ei_camera_init()) {
        Serial.println("Camera init failed!");
        while(1);
    }
    Serial.println("Camera initialized successfully");

    HTTPClient http;
    http.begin(String(serverBase) + "/");
    int code = http.GET();
    Serial.print("Server GET test code: ");
    Serial.println(code);
    http.end();
}

void loop() {
    if (!ei_camera_capture(EI_CLASSIFIER_INPUT_WIDTH, EI_CLASSIFIER_INPUT_HEIGHT)) {
        Serial.println("Capture failed");
        delay(2000);
        return;
    }

    ei::signal_t signal;
    signal.total_length = EI_CLASSIFIER_INPUT_WIDTH * EI_CLASSIFIER_INPUT_HEIGHT;
    signal.get_data = [](size_t offset, size_t length, float* out_ptr) -> int {
        return ei_camera_get_data(offset, length, out_ptr);
    };

    ei_impulse_result_t result = {0};
    if (run_classifier(&signal, &result, debug_nn) != EI_IMPULSE_OK) {
        Serial.println("Classifier failed");
        ei_camera_fb_return();
        delay(2000);
        return;
    }

    size_t max_index = 0;
    float max_value = 0;
    for (size_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        if (result.classification[i].value > max_value) {
            max_value = result.classification[i].value;
            max_index = i;
        }
    }

    String worker_id = result.classification[max_index].label;
    int weight = 5;

    if (worker_id == last_worker_id && weight == last_weight) {
        Serial.println("Same worker & weight, skipping POST.");
        ei_camera_fb_return();
        delay(5000);
        return;
    }

    last_worker_id = worker_id;
    last_weight = weight;

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(String(serverBase) + String(recognizeRoute));
        http.addHeader("Content-Type", "application/json");
        http.setTimeout(90000);

        String payload = "{\"worker_id\":\"" + worker_id + "\",\"weight\":" + String(weight) + "}";
        Serial.println("Payload: " + payload);

        int httpResponseCode = http.POST(payload);

        Serial.print("HTTP response code: ");
        Serial.println(httpResponseCode);

        if (httpResponseCode == 200) {
            String response = http.getString();
            Serial.println("Server response: " + response);
        } else {
            Serial.println("POST failed: " + http.errorToString(httpResponseCode));
            last_worker_id = "";
            last_weight = 0;
        }

        http.end();
    } else {
        Serial.println("WiFi not connected.");
        last_worker_id = "";
        last_weight = 0;
    }

    ei_camera_fb_return();
    delay(5000);
}
