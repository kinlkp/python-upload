/*
* struct_to_json.c
* Program for get linux memory metrics
* by Brian Leung
* created 2023/05/30
*/


#include "stdio.h"
#include "string.h"
#include "stdlib.h"
#include "struct_to_json.h"

/* object counter */
int counter = 0;

void StructToJSON_constructor(StructToJSON *self, char *key_and_value) {
  char temp[200];
  strcpy(temp, key_and_value);
  strcpy(self->key, strtok(temp, ":"));
  strcpy(self->value, strtok(NULL, ":"));
}

void iterate_queue_render_json(StructToJSON **sj_queue) {
  char *str_format;
  Map *map1;
  
  map1 = malloc(sizeof(Map));
  strcpy(map1->resource, "memory");
  map1->data = sj_queue;

  /* iterate the queue and print the json */
  printf("%s \"%s\":{", "{", map1->resource);
  for (int i=0; i<counter; i++) {
    if (i == counter - 1) {
      str_format = "\"%s\":\"%s\"";
    } else {
      str_format = "\"%s\":\"%s\",";
    }
    printf(str_format, (map1->data[i])->key, (map1->data[i])->value);
    /* release the previous allocated address */
    free(sj_queue[i]);
  }
  printf("%s%s", "}", "}");
}

