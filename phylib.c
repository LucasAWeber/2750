#include "phylib.h"

// CORRECT
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) {
    phylib_object * still_ball_object = malloc(sizeof(phylib_object));
    if (still_ball_object == NULL) {
        return NULL;
    }
    still_ball_object->type = 0;
    still_ball_object->obj.still_ball.number = number;
    still_ball_object->obj.still_ball.pos = *pos;
    return still_ball_object;
}

// CORRECT
phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ) {
    phylib_object * rolling_ball_object = malloc(sizeof(phylib_object));
    if (rolling_ball_object == NULL) {
        return NULL;
    }
    rolling_ball_object->type = 1;
    rolling_ball_object->obj.rolling_ball.number = number;
    rolling_ball_object->obj.rolling_ball.pos = *pos;
    rolling_ball_object->obj.rolling_ball.vel = *vel;
    rolling_ball_object->obj.rolling_ball.acc = *acc;
    return rolling_ball_object;
}

// CORRECT
phylib_object *phylib_new_hole( phylib_coord *pos ) {
    phylib_object * hole_object = malloc(sizeof(phylib_object));
    if (hole_object == NULL) {
        return NULL;
    }
    hole_object->type = 2;
    hole_object->obj.hole.pos = *pos;
    return hole_object;
}

// CORRECT
phylib_object *phylib_new_hcushion( double y ) {
    phylib_object * hcushion_object = malloc(sizeof(phylib_object));
    if (hcushion_object == NULL) {
        return NULL;
    }
    hcushion_object->type = 3;
    hcushion_object->obj.hcushion.y = y;
    return hcushion_object;
}

// CORRECT
phylib_object *phylib_new_vcushion( double x ) {
    phylib_object * vcushion_object = malloc(sizeof(phylib_object));
    if (vcushion_object == NULL) {
        return NULL;
    }
    vcushion_object->type = 4;
    vcushion_object->obj.vcushion.x = x;
    return vcushion_object;
}

// CORRECT
phylib_table *phylib_new_table( void ) {
    phylib_table * table_object = malloc(sizeof(phylib_table));
    if (table_object == NULL) {
        return NULL;
    }
    table_object->time = 0.0;
    table_object->object[0] = phylib_new_hcushion(0.0);
    table_object->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table_object->object[2] = phylib_new_vcushion(0.0);
    table_object->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    phylib_coord * pos = malloc(sizeof(phylib_coord));
    pos->x = 0.0; pos->y = 0.0;
    table_object->object[4] = phylib_new_hole(pos);
    pos->x = 0.0; pos->y = PHYLIB_TABLE_LENGTH/2.0;
    table_object->object[5] = phylib_new_hole(pos);
    pos->x = 0.0; pos->y = PHYLIB_TABLE_LENGTH;
    table_object->object[6] = phylib_new_hole(pos);
    pos->x = PHYLIB_TABLE_WIDTH; pos->y = 0.0;
    table_object->object[7] = phylib_new_hole(pos);
    pos->x = PHYLIB_TABLE_WIDTH; pos->y = PHYLIB_TABLE_LENGTH/2.0;
    table_object->object[8] = phylib_new_hole(pos);
    pos->x = PHYLIB_TABLE_WIDTH; pos->y = PHYLIB_TABLE_LENGTH;
    table_object->object[9] = phylib_new_hole(pos);
    free(pos);
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        table_object->object[i] = NULL;
    }
    return table_object;
}

// CORRECT
void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
    if (*src == NULL) {
        *dest = NULL;
        return;
    }
    *dest = malloc(sizeof(phylib_object));
    memcpy(*dest, *src, sizeof(phylib_object));
}

// CORRECT
phylib_table *phylib_copy_table( phylib_table *table ) {
    phylib_table * table_object_copy = malloc(sizeof(phylib_table));
    if (table_object_copy == NULL) {
        return NULL;
    }
    table_object_copy->time = table->time;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        phylib_copy_object(&table_object_copy->object[i], &table->object[i]);
    }
    return table_object_copy;
}

// CORRECT
void phylib_add_object( phylib_table *table, phylib_object *object ) {
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            return;
        }
    }
}

// CORRECT
void phylib_free_table( phylib_table *table ) {
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            free(table->object[i]);
        }
    }
    free(table);
}

// CORRECT
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {
    phylib_coord c3;
    c3.x = 0.0;
    c3.y = 0.0;
    c3.x = c1.x - c2.x;
    c3.y = c1.y - c2.y;
    return c3;
}

// CORRECT
double phylib_length( phylib_coord c ) {
    return sqrt(c.x * c.x + c.y * c.y);
}

// CORRECT
double phylib_dot_product( phylib_coord a, phylib_coord b ) {
    return a.x * b.x + a.y * b.y;
}

// CORRECT
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {
    if (obj1->type != 1) {
        return -1.0;
    }
    if (obj2->type == 0) {
        return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
    }
    if (obj2->type == 1) {
        return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
    }
    if (obj2->type == 2) {
        return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
    }
    if (obj2->type == 3) {
        return fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
    }
    if (obj2->type == 4) {
        return fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
    }
    return -1.0;
}

// CORRECT
void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
    if (old->type != 1 || new->type != 1) {
        return;
    }
    new->obj.rolling_ball.pos.x = 0.0 + old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + (1.0/2.0 * old->obj.rolling_ball.acc.x * (time * time));
    new->obj.rolling_ball.vel.x = 0.0 + old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    if (new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x < 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    new->obj.rolling_ball.pos.y = 0.0 + old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + (1.0/2.0 * old->obj.rolling_ball.acc.y * (time * time));
    new->obj.rolling_ball.vel.y = 0.0 + old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;
    if (new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

// CORRECT
unsigned char phylib_stopped( phylib_object *object ) {
    if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {
        phylib_coord temp_pos = object->obj.rolling_ball.pos;
        unsigned char temp_num = object->obj.rolling_ball.number;
        object->type = 0;
        object->obj.still_ball.number = temp_num;
        object->obj.still_ball.pos = temp_pos;
        return 1;
    }
    return 0;
}

// CORRECT
void phylib_bounce( phylib_object **a, phylib_object **b ) {
    switch((*b)->type) {
        case 3:
        {
            (*a)->obj.rolling_ball.vel.y *= -1.0;
            (*a)->obj.rolling_ball.acc.y *= -1.0;
            break;
        }
        case 4:
        {
            (*a)->obj.rolling_ball.vel.x *= -1.0;
            (*a)->obj.rolling_ball.acc.x *= -1.0;
            break;
        }
        case 2:
        {
            free(*a);
            *a = NULL;
            break;
        } 
        case 0:
        {
            unsigned char temp_num = (*b)->obj.still_ball.number;
            phylib_coord temp_pos = (*b)->obj.still_ball.pos;
            (*b)->type = 1;
            (*b)->obj.rolling_ball.number = temp_num;
            (*b)->obj.rolling_ball.pos = temp_pos;
            temp_pos.x = 0.0;
            temp_pos.y = 0.0;
            (*b)->obj.rolling_ball.vel = temp_pos;
            (*b)->obj.rolling_ball.acc = temp_pos;
        }
        case 1:
        {
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            double r_ab_len = phylib_length(r_ab);
            phylib_coord n;
            n.x = 0.0 + r_ab.x/r_ab_len;
            n.y = 0.0 + r_ab.y/r_ab_len;
            double v_rel_n = phylib_dot_product(v_rel, n);
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;
            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            if (speed_a > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = -1.0 * (*a)->obj.rolling_ball.vel.x / speed_a * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -1.0 * (*a)->obj.rolling_ball.vel.y / speed_a * PHYLIB_DRAG;
            }
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);
            if (speed_b > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = -1.0 * (*b)->obj.rolling_ball.vel.x / speed_b * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -1.0 * (*b)->obj.rolling_ball.vel.y / speed_b * PHYLIB_DRAG;
            }
            break;
        } 
    }
}

// CORRECT
unsigned char phylib_rolling( phylib_table *t ) {
    int count = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i] != NULL && t->object[i]->type == 1) {
            count++;
        }
    }
    return count;
}

// CORRECT
phylib_table *phylib_segment( phylib_table *table ) {
    if (phylib_rolling(table) == 0) {
        phylib_free_table(table);
        return NULL;
    }
    phylib_table * new_table = phylib_copy_table(table);

    double i;
    for (i = PHYLIB_SIM_RATE; i < PHYLIB_MAX_TIME; i += PHYLIB_SIM_RATE) {
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
            if (table->object[j] == NULL || table->object[j]->type != 1) {
                continue;
            }
            phylib_object * new;
            phylib_copy_object(&new, &new_table->object[j]);
            phylib_roll(new, new_table->object[j], PHYLIB_SIM_RATE);
            free(new_table->object[j]);
            new_table->object[j] = new;
        }
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
            if (table->object[j] == NULL || table->object[j]->type != 1) {
                continue;
            }
            for (int k = 0; k < PHYLIB_MAX_OBJECTS; k++){
                if (j != k && new_table->object[k] != NULL && phylib_distance(new_table->object[j], new_table->object[k]) < 0) {
                    phylib_bounce(&new_table->object[j], &new_table->object[k]);
                    new_table->time += i;
                    return new_table;
                }
            }
            if (phylib_stopped(new_table->object[j])) {
                new_table->time += i;
                return new_table;
            }
        }
    }
    new_table->time += i;
    return new_table;
}

// CORRECT
char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
    }
    return string;
}
