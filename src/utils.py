from pygame import Rect

def check_collision(primary_entity, check_against):
    '''
    function to check collision between primary entity and list of non primary entities
    primary_entity = Entity()
    check_against = [Entity(),...]
    returns list of Entity from check_against which collide with primary_entity
    '''
    colliding_entities = []
    for i in check_against:
        if primary_entity.rect.colliderect(i.rect):
            colliding_entities.append(i)

    return colliding_entities
