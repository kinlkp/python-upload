/*
* get_mem.c
* Program for get linux memory metrics
* by Brian Leung
* created 2023/05/29
*/

#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "stdbool.h"
#include "regex.h"
#include "struct_to_json.h"
#include "time.h"

#define MEMINFO "/proc/meminfo"
#define BUFFERSIZE 64

char *defined_metrics[] = {
  // {0x4d, 0x65, 0x6d, 0x54, 0x6f}, /* MemTo */
  "MemTo", "SwapF", "MemFr", "MemAv", "Cache", "SwapT"
};

#define QUEUE_SIZE (sizeof(defined_metrics)/sizeof(defined_metrics[0]))

/* pointer array of object StructToJSON
* QUEUE_SIZE + 1 includes timestamp in the queue
*/
StructToJSON *sj_queue[QUEUE_SIZE+1];


bool add_key_value_into_queue(char *key_and_value) {
  /*
  * assign the address to array of pointer (struct) 
  * using global variable counter to count the objects 
  * in struct_to_json.h
  */
  sj_queue[counter] = (StructToJSON *)malloc(sizeof(StructToJSON));
  StructToJSON_constructor(sj_queue[counter], key_and_value);
  /* increment the counter. Next round, work on the next item in sj_queue */
  counter++;
}

bool match_regex(char *str, const char *pattern) {
  regex_t regex;

  int reg_comp = regcomp(&regex, pattern, REG_EXTENDED);
  if (reg_comp != 0) {
    printf("Error:");
    exit(EXIT_FAILURE);
  }
  int reg_exec = regexec(&regex, str, 0, NULL, 0);
  if (reg_exec == 0) {
    return true;
  }
  return false;
} 

char *extact_key_value(char *str) {
  /* Split the string into tokens */
  char *delimiter = " ";
  char *token;

  token = strtok(str, delimiter);
  char *temp;
  /* match the metrics key */
  if (match_regex(token, "([a-zA-Z]+):")) {
    temp = token;
  }
  while (token != NULL) {
    /* match the metrics value */
    if (match_regex(token, "[0-9]+")) {
      char *key_and_value = strcat(temp, token);
      /* process string key:value */
      add_key_value_into_queue(key_and_value);
    }
    token = strtok(NULL, delimiter);
  }
}

bool get_defined_items(FILE *fp) {
  char buffer[BUFFERSIZE];

  /* Read the file until eof */
  while (!feof(fp)) {
    fgets(buffer, BUFFERSIZE, fp);
    if (buffer == NULL)
      return false;
    /* loop the metrics array and get the metrics if matched*/
    char *buffer_substr = strndup(buffer, 5);
    // int array_size = sizeof(defined_metrics)/sizeof(defined_metrics[0]);
    for (int i=0; i < QUEUE_SIZE; i++) {
      if (strcmp(buffer_substr, defined_metrics[i]) == 0){
        /* extract the value of each memory items */
        extact_key_value(buffer);
      }
    }
  }
  return true;
}

int main() {

  FILE *fp;
  /* open "/proc/meminfo" */
  fp = fopen(MEMINFO, "r");
  if (fp == NULL) {
    puts("Error: Can't open the file!");
    exit(EXIT_FAILURE);
  }
  if ( !get_defined_items(fp) ) {
    printf("Extract failed!");
    exit(EXIT_FAILURE);
  }
  fclose(fp);
  char timestamp[50];
  sprintf(timestamp, "timestamp:%lu", (unsigned long)time(NULL));
  add_key_value_into_queue(timestamp);
  /* iterate the struct queue sj_queue */
  iterate_queue_render_json(sj_queue);

/*
  struct Map m1 = {"memory", sj_queue};
  struct Map ma1[] = {{"memory", sj_queue}, {"cpu", sj_queue}};
*/
  return EXIT_SUCCESS;
}
