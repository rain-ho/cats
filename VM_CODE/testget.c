#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

#define MAX_RESPONSE_SIZE 4096

size_t curl_callback(void *contents, size_t size, size_t nmemb, char *buffer) {
    size_t total_size = size * nmemb;
    strncat(buffer, contents, total_size);
    return total_size;
}


int main(int argc, char *argv[]) {
    CURL *curl;
    CURLcode res;

    char *BASE_URL = getenv("BASE_URL");

    const char *API_KEY = getenv("API_KEY");

    curl = curl_easy_init();
    if (curl) {
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, API_KEY);

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "GET");
        curl_easy_setopt(curl, CURLOPT_URL, BASE_URL);

        // Set up response buffer
        char response_buffer[MAX_RESPONSE_SIZE];
        response_buffer[0] = '\0';

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &curl_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, response_buffer);

        res = curl_easy_perform(curl);
        // Check for errors
        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        } 
        else {
            // Extract the value from the specific column
            char *start = strstr(response_buffer, "\"riskreps\":");
            if (start != NULL) 
            {
                start += strlen("\"riskreps\":");

                char *end = strchr(start, ',');
                if (end == NULL) {
                    end = strchr(start, '}');
                }

                if (end != NULL) {
                    // Copy the value into a separate string
                    size_t length = end - start;
                    char riskreps_value[length + 1];
                    strncpy(riskreps_value, start, length);
                    riskreps_value[length] = '\0';

                    // Convert the value to an integer
                    int riskreps = atoi(riskreps_value);

                    printf("Riskreps: %d\n", riskreps);
                    return riskreps;
                } 
                else {
                    fprintf(stderr, "Invalid riskreps column\n");
                }
            } 
            else {
                fprintf(stderr, "Riskreps column not found\n");
            }
        }

        // Clean up
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    }

    return 0;
}
