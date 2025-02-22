import os, sys
import pygame
import math
import random
import time
import copy
import socket
from _thread import *
import traceback
import numpy
import func
import los
from itertools import accumulate
import ast


from values import *


def render_center(image,pos):
    im = zoom_transform(image,zoom)
    r_pos = minus([-im.get_rect().center[0],-im.get_rect().center[1]],pos)
    screen.blit(im,r_pos)

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


object_list = {}
class Object:
    def __init__(self,sub_object):
        global object_list
        self.__object = sub_object
        priority = sub_object.priority()
        if priority not in object_list:
            object_list[priority] = [self]
        else:
            object_list[priority].append(self)

    def tick(self):
        self.__object.tick()

    def kill(self):
        object_list[self.__object.priority()].remove(self)

def get_slope(point_1, point_2, y=False):
    try:
        slope = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
    except:
        slope = (point_2[1] - point_1[1]) * float("inf")

    if y:
        try:
            slope = 1/slope
        except:
            slope *= float("inf")


    return slope

def get_intersect(point,scalar,slope, y=False):
    if slope != 0:
        return point[1] + (scalar - point[0]) / slope if y else point[0] + (scalar - point[1]) / slope

    else:
        return point[1] if y else point[0]

def get_dist(point_1,point_2):
    return math.sqrt((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)

class anus:
    def priority(self):
        return "1"

    def tick(self):
        print("anus")

class pissa:
    def priority(self):
        return "2"

    def tick(self):
        print("pissa")

def PolyArea(x,y):
    return 0.5*numpy.abs(numpy.dot(x,numpy.roll(y,1))-numpy.dot(y,numpy.roll(x,1)))

def getcollisions(tiles,boxcollider):
    return (tile for tile in tiles if tile.colliderect(boxcollider))


def getcollisionspoint(tiles, point):
    return (tile for tile in tiles if tile.collidepoint(point))


class Map:
    def __init__(self,name, dir,  nav_mesh_name, pos, conv ,size,polygons,objects):
        self.name = name
        self.size = size
        self.polygons = []

        self.nav_mesh_available_spots = []

        self.conv = 1920/854

        # self.conv = conv
        self.points_inside_polygons = []
        self.pos = [pos[0] / self.conv, pos[1] / self.conv]

        self.nav_mesh_name = nav_mesh_name

        self.barricade_rects = []

        # polygons.append([-100,0,100,size[1]])
        # polygons.append([size[0],0,100,size[1]])
        # polygons.append([0,-100,size[0],100])
        # polygons.append([0,size[1],size[0],100])


        for polygon in polygons:
            x,y,width,height = polygon

            x += pos[0]
            y += pos[1]


            self.polygons.append([[(x)/ self.conv, (y+height) / self.conv],[(x) / self.conv,(y) / self.conv],[(x+width) / self.conv,(y) / self.conv],[(x+width) / self.conv,(y+height) / self.conv]])
        self.objects = objects

        self.background = pygame.transform.scale(pygame.image.load("texture/" + dir), [round(size[0] / self.conv), round(size[1] / self.conv)]).convert()

    def get_polygons(self):
        return self.polygons

    def get_size(self):
        return self.size

    def append_polygon(self, polygon):
        x,y,width,height = polygon
        self.polygons.append([[(x)/ self.conv, (y+height) / self.conv],[(x) / self.conv,(y) / self.conv],[(x+width) / self.conv,(y) / self.conv],[(x+width) / self.conv,(y+height) / self.conv]])

    def read_navmesh(self, walls_filtered):
        NAV_MESH = []
        try:
            file = open(self.nav_mesh_name, "r")
            lines = file.readlines()
            file.close()
            for line in lines:
                ref_point = {"point" : ast.literal_eval(line), "connected" : []}
                NAV_MESH.append(ref_point)
            for ref_point in NAV_MESH:
                for point_dict in NAV_MESH:
                    point = point_dict["point"]
                    if point == ref_point["point"]:
                        continue
                    if los.check_los(point, ref_point["point"], walls_filtered):
                        ref_point["connected"].append(point)


        except Exception as e:
            print(e)

        return NAV_MESH


    def checkcollision(self, pos, movement,collider_size, map_size, damage_barricades = False, damager = None, ignore_barricades = False, collider_rect = False, check_only_collision = False):
        if collider_rect:
            collider = pos
        else:
            collider = pygame.Rect(pos[0]-collider_size,pos[1]-collider_size, collider_size*2, collider_size*2)
        map_rect = pygame.Rect(0,0,map_size[0], map_size[1])

        collisiontypes = {

        "left": False,

        "right": False,

        "top": False,

        "bottom": False

        }

        if collider.centerx < collider_size:
            collider.left = 0

            collisiontypes["left"] = True

        if collider.centerx > map_size[0] - collider_size:
            collider.right = map_size[0]

            collisiontypes["right"] = True

        if collider.centery < collider_size:
            collider.top = 0

            collisiontypes["top"] = True

        if collider.centery > map_size[1] - collider_size:
            collider.bottom = map_size[1]

            collisiontypes["bottom"] = True






        # if not map_rect.collidepoint(collider.midleft) and map_rect.collidepoint(collider.midright):
        #
        #     collider.left = map_rect.left
        #
        #     collisiontypes["right"] = True
        #
        # if not map_rect.collidepoint(collider.midright) and map_rect.collidepoint(collider.midleft):
        #
        #     collider.right = map_rect.right
        #
        #     collisiontypes["left"] = True
        #
        #
        # if not map_rect.collidepoint(collider.midbottom):
        #
        #     collider.bottom = map_rect.bottom
        #
        #     collisiontypes["bottom"] = True
        #
        # if not map_rect.collidepoint(collider.midtop):
        #
        #     collider.top = map_rect.top
        #
        #     collisiontypes["top"] = True

        if abs(movement[0]) >= abs(movement[1]):
            check_order = ["x","y"]
        else:
            check_order = ["y","x"]


        for check in check_order:


            collisions = list(getcollisions(self.rectangles,collider))

            if check == check_order[0] and damage_barricades:
                for barr in self.barricade_rects:
                    if barr[0] in getcollisions(self.rectangles,collider):
                        barr[1].__dict__["hp"] -= damager.__dict__["damage"]
                        damager.__dict__["attack_tick"] = 30




            for tile in collisions:
                if check == "x":
                    if ignore_barricades:
                        ignore = any(barr[0] == tile for barr in self.barricade_rects)
                        if ignore:
                            continue


                    if tile.collidepoint(collider.midright) and not tile.collidepoint(collider.midleft):

                        collider.right = tile.left

                        collisiontypes["right"] = True

                    if tile.collidepoint(collider.midleft) and not tile.collidepoint(collider.midright):

                        collider.left = tile.right

                        collisiontypes["left"] = True

                elif check == "y":
                    if ignore_barricades:
                        ignore = any(barr[0] == tile for barr in self.barricade_rects)
                        if ignore:
                            continue


                    if tile.collidepoint(collider.midbottom) and not tile.collidepoint(collider.midtop):

                        collider.bottom = tile.top

                        collisiontypes["bottom"] = True

                    if tile.collidepoint(collider.midtop) and not tile.collidepoint(collider.midbottom):

                        collider.top = tile.bottom

                        collisiontypes["top"] = True

        if collisiontypes != {"left": False,"right": False,"top": False,"bottom": False}:

            pos = list(collider.center)

        return collisiontypes, pos


    def generate_wall_structure(self):
        print("CHECKING POINTS INSIDE WALLS")
        polygons_temp = []
        polygons_temp.append([pygame.Rect(0,0, self.size[0], 10), []])
        polygons_temp.append([pygame.Rect(0,0, 10, self.size[1]), []])
        polygons_temp.append([pygame.Rect((self.size[0]-10)/ self.conv ,0, 15, self.size[1]/ self.conv ), []])
        polygons_temp.append([pygame.Rect(0,(self.size[1]-10)/ self.conv , self.size[0]/ self.conv , 14), []])
        self.rectangles = []
        for polygon in self.polygons:
            a,b,c,d = polygon
            x = [a[0],b[0],c[0],d[0]]
            y = [a[1],b[1],c[1],d[1]]
            poly = pygame.Rect(min(x),min(y), max(x)-min(x), max(y) - min(y))

            self.rectangles.append(poly)

            polygons_temp.append([poly,[a,b,c,d]])

        self.connected_polygons = {}
        for polygon in self.polygons:
            for point in polygon:
                for poly, points in polygons_temp:

                    if point in points:
                        continue

                    if poly.collidepoint(point):
                        self.points_inside_polygons.append(point)

                        break


        print("POINTS INSIDE:", len(self.points_inside_polygons))
        print("POINTS TOTAL:", points)






        print("GENERATING WALL STRUCTURE")
        walls = []
        for polygon in self.polygons:
            a,b,c,d = polygon
            # a = ratio(a,size_ratio)
            # b = ratio(b,size_ratio)
            # c = ratio(c,size_ratio)
            # d = ratio(d,size_ratio)
            walls.append(los.Wall(a,b))
            walls.append(los.Wall(b,c))
            walls.append(los.Wall(c,d))
            walls.append(los.Wall(d,a))

        intersecting_walls = []

        for wall_1 in walls:
            wall_points = wall_1.get_points()
            wp1, wp2 = wall_points

            mode = "vert" if wp1[0] == wp2[0] else "hor"
            for wall_2 in walls:
                wall_points = wall_1.get_points()
                p1, p2 = wall_2.get_points()

                if mode == "vert":
                    if p1[0] != p2[0]:
                        continue
                else:
                    if p1[1] != p2[1]:
                        continue
                if p1 in wall_points or p2 in wall_points:
                    continue
                if los.intersect(wall_points[0], wall_points[1], func.minus(p1,[-2,-2]), func.minus(p2,[2,2])):
                    intersecting_walls.append([wall_1, wall_2])
        # for wall_1, wall_2 in intersecting_walls:
                    a,b = wall_1.get_points()
                    c,d = wall_2.get_points()

                    res_key = min([a,b], key=lambda x: sum(x))
                    res_key2 = min([c,d], key=lambda x: sum(x))
                    res_key_max = max([a,b], key=lambda x: sum(x))
                    res_key_max2 = max([c,d], key=lambda x: sum(x))
                    wall_1.set_new_points(res_key,res_key2)
                    wall_2.set_new_points(res_key_max,res_key_max2)
        remove_list = []
        # for wall_1 in walls:
        #     a,b = wall_1.get_points()
        #     if los.get_dist_points(a, b) < 2:
        #         remove_list.append(wall_1)


        for wall_1 in walls:
            for wall_2 in walls:
                if wall_2 in remove_list:
                    continue
                wall_1_points = wall_1.get_points()
                interlink1 = None
                interlink2 = None

                for point in wall_1_points:
                    for point2 in wall_2.get_points():
                        if los.get_dist_points(point,point2) < 5:
                            interlink1 = point
                            interlink2 = point2



                if interlink1 != None and interlink2 != None:
                    wall_points = list(wall_1.get_points())
                    wall_points_2 = list(wall_2.get_points())

                    wall_points.remove(interlink1)
                    wall_points_2.remove(interlink2)

                    if los.intersect(wall_points[0], wall_points_2[0], func.minus(interlink1,[-2,-2]), func.minus(interlink1,[2,2])):
                        remove_list.append(wall_2)
                        wall_1.set_new_points(wall_points[0], wall_points_2[0])


        for wall_1 in remove_list:
            walls.remove(wall_1)

        return walls


    def check_collision2(self,player_pos, map_boundaries, return_only_collision = False, collision_box = 0, screen = screen ,x_vel = 0, y_vel = 0, dir_coll = False, phase = 0):
        collision_box_size = collision_box

        collide = False
        collides = 0
        vert_coll, hor_coll = False, False
        closest_point = None
        x5,y5 = player_pos

        map_poly = pygame.Rect(collision_box_size,collision_box_size, map_boundaries[0] - collision_box_size, map_boundaries[1] - collision_box_size)
        if not map_poly.collidepoint([x5,y5]):
            if collision_box > player_pos[0]:
                x5 = collision_box
                collide = True
                vert_coll = True

            if map_boundaries[0] - collision_box < player_pos[0]:
                x5 = map_boundaries[0] - collision_box
                vert_coll = True
                collide = True
            if collision_box > player_pos[1]:
                y5 = collision_box
                collide = True
                hor_coll = True
            if map_boundaries[1] - collision_box < player_pos[1]:
                y5 = map_boundaries[1] - collision_box
                collide = True
                hor_coll = True

        player_pos_der = [x5,y5]

        for polygon in self.polygons:
            a,b,c,d = polygon
            x = [a[0],b[0],c[0],d[0]]
            y = [a[1],b[1],c[1],d[1]]

            if player_pos[0] < min(x)-2*collision_box_size or player_pos[0] > max(x)+2*collision_box_size or player_pos[1] < min(y)-2*collision_box_size or player_pos[1] > max(y)+2*collision_box_size:
                continue

            poly = pygame.Rect(min(x)- collision_box_size,min(y) - collision_box_size, max(x)-min(x) + collision_box_size*2, max(y) - min(y) + collision_box_size*2)

            if poly.collidepoint(player_pos_der):
                pass







    def check_collision(self,player_pos, map_boundaries, return_only_collision = False, collision_box = 0, screen = screen ,x_vel = 0, y_vel = 0, dir_coll = False, phase = 0):

        collision_box_size = collision_box

        collide = False
        collides = 0
        vert_coll, hor_coll = False, False
        closest_point = None

        x5,y5 = player_pos

        if collision_box > player_pos[0]:
            x5 = collision_box
            collide = True
            vert_coll = True

        if map_boundaries[0] - collision_box < player_pos[0]:
            x5 = map_boundaries[0] - collision_box
            vert_coll = True
            collide = True
        if collision_box > player_pos[1]:
            y5 = collision_box
            collide = True
            hor_coll = True
        if map_boundaries[1] - collision_box < player_pos[1]:
            y5 = map_boundaries[1] - collision_box
            collide = True
            hor_coll = True

        # if collide and not dir_coll:
        #
        #     return [x5,y5]




        player_pos_der = [x5,y5]

        #pygame.draw.rect(screen,[255,0,0], [player_pos[0]-collision_box_size,player_pos[1]-collision_box_size,collision_box_size,collision_box_size])


        for polygon in self.polygons:
            a,b,c,d = polygon
            x = [a[0],b[0],c[0],d[0]]
            y = [a[1],b[1],c[1],d[1]]

            if player_pos[0] < min(x)-50 or player_pos[0] > max(x)+50 or player_pos[1] < min(y)-50 or player_pos[1] > max(y)+50:
                continue
            poly = pygame.Rect(min(x)- collision_box_size,min(y) - collision_box_size, max(x)-min(x) + collision_box_size*2, max(y) - min(y) + collision_box_size*2)

            minx,maxx,miny,maxy = min(x) - collision_box_size, max(x) + collision_box_size, min(y) - collision_box_size, max(y) + collision_box_size

            #pygame.draw.rect(screen,[255,255,0], [min(x)- collision_box_size,min(y) - collision_box_size, max(x)-min(x) + collision_box_size*2, max(y) - min(y) + collision_box_size*2])

            if poly.collidepoint(player_pos_der):

                collides += 1

                collide = True

                closest = 1000
                for line in range(4):
                    x1,y1 = [a,b,c,d][line]

                    x2,y2 = [a,b,c,d,a][line+1]

                    if [x1,y1] in self.points_inside_polygons and [x2,y2] in self.points_inside_polygons:
                        continue


                    x3,y3 = player_pos_der

                    dx = x2 - x1
                    dy = y2 - y1

                    alpha = (dy * y3 - dy * y1 + dx * x3 - dx * x1) / (dy ** 2 + dx ** 2)
                    #beta = (dy * x3 - dy * x1 - dx * y3 + dx * y1) / (dy ** 2 + dx ** 2)



                    x4 = x1+alpha*dx
                    y4 = y1+alpha*dy

                    dist_to_player = get_dist(player_pos, [x4,y4])
                    if dist_to_player < closest:
                        closest = dist_to_player
                        closest_line = [[x1,y1],[x2,y2]]





                if minx < player_pos_der[0] < maxx and closest_line[0][0] == closest_line[1][0]:
                    player_pos_der[0] = func.get_closest_value(player_pos_der[0],[minx, maxx])
                    vert_coll = True

                if miny < player_pos_der[1] < maxy and closest_line[0][1] == closest_line[1][1]:
                    player_pos_der[1] = func.get_closest_value(player_pos_der[1],[miny, maxy])
                    hor_coll = True




        if dir_coll:

            if player_pos_der != player_pos:

                return player_pos_der, vert_coll, hor_coll
            else:
                return False, vert_coll, hor_coll

        if not return_only_collision:
            return player_pos_der
        else:
            if collide:

                return player_pos_der
            return False




                #
                #
                #
                # x4,y4 = closest_point
                #
                # angle = math.atan2(y4 - player_pos_der[1], x4 - player_pos_der[0]) + math.pi
                # x4 += math.cos(angle) * (collision_box_size+1)
                # y4 += math.sin(angle) * (collision_box_size+1)
                #
                # if x5 == 0 and y5 == 0:
                #     x5,y5 = x4,y4
                # else:
                #     x5 = (x4+x5)/2
                #     y5 = (y4+y5)/2
                #
                # print("MOVING X BY: ", x5-player_pos_der[0],"MOVING Y BY: ", y5-player_pos_der[1])
                #
                # player_pos_der = [x5,y5]





        return player_pos_der



    def compile_navmesh(self, conv):
        for x1 in range(round(self.size[0] / 100) + 1):
            for y1 in range(round(self.size[1] / 100) + 1):
                point = [x1*100/conv,y1*100/conv]
                point[0] += 15
                point[1] += 15


                collision = False

                for polygon in self.polygons:
                    a,b,c,d = polygon
                    x = [a[0],b[0],c[0],d[0]]
                    y = [a[1],b[1],c[1],d[1]]

                    poly = pygame.Rect(min(x),min(y), max(x)-min(x), max(y) - min(y))

                    if poly.collidepoint(point):
                        collision = True
                        break
                if not collision:
                    self.nav_mesh_available_spots.append(point)



    def get_random_point(self, walls, p_pos = None, enemies = None, visibility = True, max_tries = 100):
        tries = 0
        while True:
            tries += 1
            point = func.pick_random_from_list(self.nav_mesh_available_spots)
            conds = [True, True]
            if p_pos != None:
                if los.check_los(p_pos, point, walls):
                    conds[0] = False
            if enemies != None:
                for x in enemies:
                    if los.check_los(point, x.get_pos(), walls):
                        conds[1] = False
                        break

            if False not in conds or tries > max_tries:
                return point






    def render(self, conv):

        self.map_rendered = pygame.Surface([self.size[0]/self.conv, self.size[1]/self.conv])
        self.map_rendered.fill([255,255,255])

        self.textures = {
        "floor_tile_1" : pygame.image.load("texture/floor.png").convert_alpha()
        }


        self.map_rendered.blit(self.background,(0,0))




        # for object in self.objects:   ### ((0,0),"floor_tile_1",180)
        #     object_texture = self.textures[object[1]]
        #     if object[2] != 0:
        #         rotated_image, new_rect = rot_center(object_texture,object[2],object[0][0],object[0][1])
        #         object_pos = [object[0][0] - new_rect[0], object[0][1] - new_rect[1]]
        #     else:
        #         object_pos = object[0]
        #         rotated_image = object_texture
        #     self.map_rendered.blit(rotated_image, object_pos)

        for polygon in self.polygons:
            print(polygon)
            #pygame.draw.polygon(self.map_rendered, [0,0,0], polygon)

        for point in self.nav_mesh_available_spots:
            pygame.draw.rect(self.map_rendered, [255,0,0], [point[0], point[1], 1,1])


        self.map_rendered_alpha = self.map_rendered.copy()
        self.map_rendered_alpha.set_alpha(3)

        return self.map_rendered



def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

map = (
        # # Border
        # {"a":{"x":0,"y":0}, "b":{"x":size[0],"y":0}},
        # {"a":{"x":size[0],"y":0}, "b":{"x":size[0],"y":size[1]}},
        # {"a":{"x":size[0],"y":size[1]}, "b":{"x":0,"y":size[1]}},
        # {"a":{"x":0,"y":size[1]}, "b":{"x":0,"y":0}},

        # Polygon #1
        {"a":{"x":100,"y":100}, "b":{"x":300,"y":100}},
        {"a":{"x":300,"y":100}, "b":{"x":300,"y":300}},
        {"a":{"x":300,"y":300}, "b":{"x":100,"y":300}},
        {"a":{"x":100,"y":300}, "b":{"x":100,"y":100}},

        # Polygon #1
        {"a":{"x":700,"y":100}, "b":{"x":800,"y":100}},
        {"a":{"x":800,"y":100}, "b":{"x":800,"y":300}},
        {"a":{"x":800,"y":300}, "b":{"x":700,"y":300}},
        {"a":{"x":700,"y":300}, "b":{"x":700,"y":100}},


)
