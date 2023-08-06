
// COMPILE WITH gcc -o post post.c -lcurl

#include <stdio.h>
#include <curl/curl.h>


int main(int argc, char *argv[]) {
    CURL *curl;
    CURLcode res;

    char* temp = argv[1];
    char* hum = argv[2];
    char* light = argv[3];


    char *BASE_URL = getenv("BASE_URL");

    const char *API_KEY = getenv("API_KEY");

    // Your JSON payload data for the insert request
    char *json_data[256];

    sprintf(json_data, "{\"artwork_a_id\": %s, \"temperature\": %s, \"humidity\": %s, \"vibration\": %s}",
            "10", temp, hum, light);

    curl = curl_easy_init();
    if (curl) {
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, API_KEY);

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PATCH");
        curl_easy_setopt(curl, CURLOPT_URL, BASE_URL);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data);

        res = curl_easy_perform(curl);

        // Check for errors 
        if (res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        // Clean up 
        curl_easy_cleanup(curl);

        
    }

    return 0;
}