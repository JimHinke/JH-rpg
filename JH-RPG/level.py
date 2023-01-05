import pygame
from player import Player
from file_load import *
from random import choice

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visable_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.TILESIZE = 64
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('jh-rpg/graphics/floor_Floorblocks.csv'),
            'grass': import_csv_layout('jh-rpg/graphics/floor_grass.csv'),
            'object': import_csv_layout('jh-rpg/graphics/floor_objects.csv')
        }
        image_folder = {
            'grass': import_folder('jh-rpg/graphics/Grass'),
            'objects': import_folder('jh-rpg/graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * self.TILESIZE
                        y = row_index * self.TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisable')
                        if style == 'grass':
                            random_grass_image = choice(image_folder['grass'])
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'grass',random_grass_image)
                        if style == 'object':
                            surf = image_folder['objects'][int(col)]
                            Tile((x,y),[self.visable_sprites,self.obstacle_sprites],'object',surf)

        self.player = Player((450,300),[self.visable_sprites], self.obstacle_sprites,self.create_attack,self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visable_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()

class Camera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
        #Skapar golvet
        self.floor_surf = pygame.image.load('jh-rpg/graphics/map/floor.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft =(0,0))

    def custom_draw(self,player):

        #Får offsetten
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #Ritar golvet
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((64,64))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] -64))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10,-10)

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]

        full_path = f'jh-rpg/graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.center + pygame.math.Vector2(-10,0))