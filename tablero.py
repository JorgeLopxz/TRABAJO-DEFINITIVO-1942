"""
Created by Jorge Lopez in
Universidad Carlos III de Madrid
"""

import random
import pyxel

from Proyectil import proyectil
from Proyectil import misil_REGULAR
from Proyectil import MisilSuperbombardero
from avion import avion
import constantes
from enemigos import Regular
from enemigos import Rojo
from enemigos import Superbombardero
from enemigos import Bombardero
from enemigos import MiniBoss
from islas import islas


class Tablero:
    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        pyxel.init(self.ancho, self.alto, title="1942 Reforged")

        self.decorado_islas = [islas(*i) for i in constantes.islas]
        self.stars = self._crear_estrellas()

        self._reset_game_state()
        pyxel.run(self.update, self.draw)

    def _reset_game_state(self):
        self.avion = avion((self.ancho // 2), 200)
        self.puntuacion = 0
        self.recordpuntuacion = max(getattr(self, "recordpuntuacion", 0), 0)
        self.distancia = 0

        self.inicio = False
        self.game_over = False

        self.misilesavion_list = []
        self.misilesregular_list = []
        self.misilesbombardero_list = []
        self.misilesSuperbombardero_list = []

        self.regList = []
        self.rojoList = []
        self.bombarderoList = []
        self.superBombarderoList = []

        self.miniboss = None
        self.next_miniboss_score = 250
        self.next_miniboss_distance = 1800

        self.weapon_mode = "normal"
        self.weapon_timer = 0
        self.fire_timer = 0
        self.perks = []

        self.choice = 1
        self.loop_cooldown = 0

        self.death_frames = 0
        self.pending_respawn = False
        self.explosion_particles = []

    def _crear_estrellas(self):
        stars = []
        for _ in range(70):
            stars.append(
                {
                    "x": random.randint(0, self.ancho - 1),
                    "y": random.randint(0, self.alto - 1),
                    "speed": random.choice((0.2, 0.4, 0.6, 0.9)),
                    "color": random.choice((5, 6, 7, 12)),
                }
            )
        return stars

    def _rect_overlap(self, a, b):
        return (
            a[0] < b[0] + b[2]
            and a[0] + a[2] > b[0]
            and a[1] < b[1] + b[3]
            and a[1] + a[3] > b[1]
        )

    def _player_bbox(self):
        return (int(self.avion.x), int(self.avion.y), 22, 16)

    def _spawn_explosion(self, x, y, power=22):
        for _ in range(power):
            self.explosion_particles.append(
                {
                    "x": x + random.randint(-8, 8),
                    "y": y + random.randint(-8, 8),
                    "vx": random.uniform(-1.8, 1.8),
                    "vy": random.uniform(-2.2, 1.5),
                    "life": random.randint(16, 28),
                    "color": random.choice((8, 9, 10, 7, 15)),
                }
            )

    def _damage_player(self):
        if self.avion.invulnerable_frames > 0 or self.death_frames > 0 or self.game_over:
            return

        self.avion.vidas -= 1
        self._spawn_explosion(self.avion.x + 10, self.avion.y + 8)
        self.death_frames = 26

        if self.avion.vidas <= 0:
            self.game_over = True
            return

        self.pending_respawn = True

    def _respawn_player(self):
        self.avion.x = self.ancho // 2 - 10
        self.avion.y = 205
        self.avion.invulnerable_frames = 120

    def _active_fire_profile(self):
        if self.weapon_mode == "double":
            return {"cooldown": 8, "speed": 12, "damage": 1, "type": "normal", "offsets": (-6, 6)}
        if self.weapon_mode == "rapid":
            return {"cooldown": 4, "speed": 12, "damage": 1, "type": "normal", "offsets": (0,)}
        if self.weapon_mode == "laser":
            return {"cooldown": 6, "speed": 15, "damage": 2, "type": "laser", "offsets": (0,)}
        return {"cooldown": 8, "speed": 12, "damage": 1, "type": "normal", "offsets": (0,)}

    def _fire_player(self):
        if self.death_frames > 0 or self.game_over:
            return

        profile = self._active_fire_profile()
        for offset in profile["offsets"]:
            self.misilesavion_list.append(
                proyectil(
                    self.avion.x + 11 + offset,
                    self.avion.y - 4,
                    velocidad=profile["speed"],
                    damage=profile["damage"],
                    tipo=profile["type"],
                )
            )
        self.fire_timer = profile["cooldown"]

    def _apply_perk(self, perk_type):
        self.weapon_mode = perk_type
        self.weapon_timer = 900
        self.puntuacion += 5

    def _spawn_perk(self):
        if len(self.perks) >= 2:
            return
        perk_type = random.choice(("double", "rapid", "laser"))
        self.perks.append(
            {
                "x": random.randint(24, self.ancho - 24),
                "y": -12,
                "vy": random.uniform(0.7, 1.2),
                "type": perk_type,
            }
        )

    def _spawn_miniboss_if_needed(self):
        if self.miniboss is not None or not self.inicio or self.game_over:
            return

        if self.puntuacion >= self.next_miniboss_score or self.distancia >= self.next_miniboss_distance:
            self.miniboss = MiniBoss((self.ancho // 2) - 24, -40)
            self.next_miniboss_score += 500
            self.next_miniboss_distance += 2200

    def _update_background(self):
        for star in self.stars:
            star["y"] += star["speed"]
            if star["y"] >= self.alto:
                star["x"] = random.randint(0, self.ancho - 1)
                star["y"] = 0

    def _update_particles(self):
        alive = []
        for p in self.explosion_particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.04
            p["life"] -= 1
            if p["life"] > 0:
                alive.append(p)
        self.explosion_particles = alive

    def _update_perks(self):
        if self.weapon_timer > 0:
            self.weapon_timer -= 1
            if self.weapon_timer == 0:
                self.weapon_mode = "normal"

        if self.inicio and not self.game_over and pyxel.frame_count % 420 == 0 and random.random() < 0.4:
            self._spawn_perk()

        player_box = self._player_bbox()
        remaining = []
        for perk in self.perks:
            perk["y"] += perk["vy"]
            perk_box = (int(perk["x"] - 6), int(perk["y"] - 6), 12, 12)
            if perk["y"] > self.alto + 10:
                continue
            if self.death_frames == 0 and self._rect_overlap(player_box, perk_box):
                self._apply_perk(perk["type"])
                continue
            remaining.append(perk)
        self.perks = remaining

    def _spawn_enemies(self):
        difficulty = min(5, self.puntuacion // 120)

        if pyxel.frame_count % max(80, 130 - difficulty * 8) == 0 and len(self.regList) < (4 + difficulty):
            x = random.randint(15, self.ancho - 30)
            self.regList.append(Regular(x, -12, "REGULAR"))

        if pyxel.frame_count % 250 == 0 and len(self.rojoList) < 6:
            for i in range(4):
                self.rojoList.append(Rojo(-30 - i * 20, random.randint(40, 90), "ROJO"))

        if pyxel.frame_count % 340 == 0 and len(self.bombarderoList) < 2:
            b = Bombardero(random.randint(20, self.ancho - 40), -20, "BOMBARDERO")
            b.vidas = 8
            self.bombarderoList.append(b)

        if pyxel.frame_count % 460 == 0 and len(self.superBombarderoList) < 2:
            sb = Superbombardero(random.randint(30, self.ancho - 60), self.alto + 10, "SUPERBOMBARDERO")
            sb.vidas = 12
            self.superBombarderoList.append(sb)

    def _update_enemy_logic(self):
        player_x = self.avion.x + 10
        player_y = self.avion.y + 8

        for enemy in self.regList:
            enemy.movimiento(enemy.y, player_x, enemy.x)
            if pyxel.frame_count % 90 == 0 and random.random() < 0.35:
                self.misilesregular_list.append(misil_REGULAR(enemy.x + 8, enemy.y + 8))

        for enemy in self.rojoList:
            enemy.movimiento()

        for enemy in self.bombarderoList:
            enemy.movimiento(enemy.y)
            if pyxel.frame_count % 80 == 0 and random.random() < 0.4:
                self.misilesbombardero_list.append(misil_REGULAR(enemy.x + 12, enemy.y + 8))

        for enemy in self.superBombarderoList:
            enemy.movimiento(enemy.y, random.randint(45, 95))
            if pyxel.frame_count % 100 == 0:
                self.misilesSuperbombardero_list.append(MisilSuperbombardero(enemy.x + 12, enemy.y + 16))

        if self.miniboss is not None:
            self.miniboss.movimiento()
            if self.miniboss.disparo_cooldown > 0:
                self.miniboss.disparo_cooldown -= 1
            else:
                for spread in (-2, 0, 2):
                    m = misil_REGULAR(self.miniboss.x + 24 + spread * 4, self.miniboss.y + 20)
                    m.fase_persecucion = 5
                    m.deriva_horizontal = spread
                    m.velocidad = 2.2
                    self.misilesbombardero_list.append(m)
                self.miniboss.disparo_cooldown = 36

        for m in self.misilesregular_list:
            m.movimiento(player_x, player_y)
        for m in self.misilesbombardero_list:
            m.movimiento(player_x, player_y)

        for m in self.misilesSuperbombardero_list:
            if self.choice == 1:
                m.movimiento1()
            elif self.choice == 2:
                m.movimiento2()
            else:
                m.movimiento3()
            self.choice += 1
            if self.choice > 3:
                self.choice = 1

        self.regList = [e for e in self.regList if -30 <= e.y <= self.alto + 40 and -40 <= e.x <= self.ancho + 40]
        self.rojoList = [e for e in self.rojoList if -60 <= e.y <= self.alto + 40 and -60 <= e.x <= self.ancho + 60]
        self.bombarderoList = [e for e in self.bombarderoList if -60 <= e.y <= self.alto + 60 and -80 <= e.x <= self.ancho + 80]
        self.superBombarderoList = [e for e in self.superBombarderoList if -80 <= e.y <= self.alto + 80 and -80 <= e.x <= self.ancho + 80]

        self.misilesavion_list = [m for m in self.misilesavion_list if m.y > -30]
        self.misilesregular_list = [m for m in self.misilesregular_list if -20 <= m.y <= self.alto + 20 and -20 <= m.x <= self.ancho + 20]
        self.misilesbombardero_list = [m for m in self.misilesbombardero_list if -20 <= m.y <= self.alto + 20 and -20 <= m.x <= self.ancho + 20]
        self.misilesSuperbombardero_list = [m for m in self.misilesSuperbombardero_list if -20 <= m.y <= self.alto + 20 and -20 <= m.x <= self.ancho + 20]

    def _handle_collisions(self):
        player_box = self._player_bbox()

        for bullet in list(self.misilesavion_list):
            bullet_box = (int(bullet.x - 2), int(bullet.y - 6), 8, 14)
            hit = False

            for enemy_list, box in (
                (self.regList, (18, 14)),
                (self.rojoList, (18, 16)),
                (self.bombarderoList, (30, 18)),
                (self.superBombarderoList, (34, 30)),
            ):
                for enemy in list(enemy_list):
                    enemy_box = (int(enemy.x), int(enemy.y), box[0], box[1])
                    if self._rect_overlap(bullet_box, enemy_box):
                        enemy.vidas = getattr(enemy, "vidas", 1) - bullet.damage
                        if enemy.vidas <= 0:
                            enemy_list.remove(enemy)
                            self.puntuacion += 10 if enemy.tipo == "REGULAR" else 18
                            if enemy.tipo == "BOMBARDERO":
                                self.puntuacion += 20
                            if enemy.tipo == "SUPERBOMBARDERO":
                                self.puntuacion += 35
                            self._spawn_explosion(enemy.x + box[0] // 2, enemy.y + box[1] // 2, power=14)
                        hit = True
                        break
                if hit:
                    break

            if self.miniboss is not None and not hit:
                boss_box = (int(self.miniboss.x), int(self.miniboss.y), self.miniboss.size_avion_x, self.miniboss.size_avion_y)
                if self._rect_overlap(bullet_box, boss_box):
                    self.miniboss.vidas -= bullet.damage
                    self.puntuacion += 2
                    hit = True
                    if self.miniboss.vidas <= 0:
                        self._spawn_explosion(self.miniboss.x + 22, self.miniboss.y + 14, power=40)
                        self.puntuacion += 180
                        self.miniboss = None
                        self._spawn_perk()

            if hit and bullet in self.misilesavion_list:
                self.misilesavion_list.remove(bullet)

        if self.death_frames == 0 and self.avion.invulnerable_frames == 0 and not self.game_over:
            for missile_list in (self.misilesregular_list, self.misilesbombardero_list, self.misilesSuperbombardero_list):
                for m in list(missile_list):
                    missile_box = (int(m.x - 2), int(m.y - 2), 6, 6)
                    if self._rect_overlap(player_box, missile_box):
                        missile_list.remove(m)
                        self._damage_player()
                        break

            for enemy, box in (
                (self.regList, (18, 14)),
                (self.rojoList, (18, 16)),
                (self.bombarderoList, (30, 18)),
                (self.superBombarderoList, (34, 30)),
            ):
                for e in enemy:
                    if self._rect_overlap(player_box, (int(e.x), int(e.y), box[0], box[1])):
                        self._damage_player()
                        return

            if self.miniboss is not None:
                boss_box = (int(self.miniboss.x), int(self.miniboss.y), self.miniboss.size_avion_x, self.miniboss.size_avion_y)
                if self._rect_overlap(player_box, boss_box):
                    self._damage_player()

    def _draw_background(self):
        pyxel.cls(1)

        for y in range(self.alto):
            if y < 56:
                color = 1 if y % 3 else 0
            elif y < 170:
                color = 2 if y % 4 else 1
            else:
                color = 3 if y % 2 else 2
            pyxel.line(0, y, self.ancho, y, color)

        for star in self.stars:
            pyxel.pset(star["x"], star["y"], star["color"])

        drift = pyxel.frame_count % (self.alto + 560)
        for deco in self.decorado_islas:
            x = int(deco.x)
            y = int(deco.y + drift)
            if -40 <= y <= self.alto + 40:
                if "nube" in deco.tipo:
                    pyxel.circ(x + 10, y + 5, 6, 7)
                    pyxel.circ(x + 18, y + 8, 7, 6)
                    pyxel.circ(x + 25, y + 6, 5, 7)
                else:
                    pyxel.tri(x, y + 18, x + 14, y, x + 30, y + 18, 3)
                    pyxel.rect(x + 8, y + 15, 18, 8, 11)
                    pyxel.rect(x + 10, y + 17, 14, 4, 10)

    def _draw_start_screen(self):
        self._draw_background()
        blink = (pyxel.frame_count // 18) % 2 == 0

        pyxel.rect(18, 42, 220, 148, 0)
        pyxel.rectb(18, 42, 220, 148, 8)
        pyxel.text(88, 58, "1942 REFORGED", 10)
        pyxel.text(58, 84, "CAMPANA ARCADE MEJORADA", 7)
        pyxel.text(40, 104, "MOVER: FLECHAS   DISPARO: ESPACIO", 6)
        pyxel.text(40, 116, "LOOPING: X (INVULNERABLE CORTO)", 9)
        pyxel.text(40, 128, "PERKS: DOUBLE / RAPID / LASER", 11)
        pyxel.text(40, 140, "SOBREVIVE HASTA EL MINI BOSS", 14)
        if blink:
            pyxel.text(70, 166, "PULSA M PARA COMENZAR", 7)

    def _draw_player(self):
        if self.death_frames > 0:
            return

        if self.avion.invulnerable_frames > 0 and (pyxel.frame_count // 4) % 2 == 0:
            return

        x = int(self.avion.x)
        y = int(self.avion.y)

        if self.avion.rodando and self.avion.rodando_duracion > 0:
            phase = 1 - (self.avion.rodando_frames / self.avion.rodando_duracion)
            radius = 6 + int(4 * pyxel.sin(phase * 360))
            pyxel.circb(x + 10, y + 8, max(4, radius), 8)
            pyxel.tri(x + 10, y - 2, x + 4, y + 14, x + 16, y + 14, 7)
            pyxel.rect(x + 8, y + 4, 4, 10, 10)
            return

        tilt = 0
        if self.avion.ultima_direccion_horizontal == "izquierda":
            tilt = -2
        elif self.avion.ultima_direccion_horizontal == "derecha":
            tilt = 2

        pyxel.tri(x + 10 + tilt, y - 1, x + 3 + tilt, y + 14, x + 17 + tilt, y + 14, 7)
        pyxel.tri(x + 10 + tilt, y + 2, x + 6 + tilt, y + 9, x + 14 + tilt, y + 9, 12)
        pyxel.rect(x + 9 + tilt, y + 9, 3, 7, 10)
        pyxel.pset(x + 10 + tilt, y + 1, 8)

        if pyxel.btn(pyxel.KEY_SPACE):
            pyxel.rect(x + 9 + tilt, y + 16, 3, 3, 9)

    def _draw_enemy(self, enemy, kind):
        x = int(enemy.x)
        y = int(enemy.y)

        if kind == "REGULAR":
            pyxel.tri(x + 8, y, x, y + 12, x + 16, y + 12, 8)
            pyxel.rect(x + 7, y + 8, 2, 6, 10)
        elif kind == "ROJO":
            pyxel.tri(x + 9, y, x + 1, y + 13, x + 17, y + 13, 9)
            pyxel.rect(x + 8, y + 7, 3, 7, 8)
        elif kind == "BOMBARDERO":
            pyxel.rect(x + 4, y + 3, 22, 10, 4)
            pyxel.tri(x + 14, y - 2, x + 2, y + 10, x + 26, y + 10, 8)
            pyxel.rect(x + 12, y + 10, 4, 7, 10)
        elif kind == "SUPERBOMBARDERO":
            pyxel.rect(x + 2, y + 5, 30, 12, 5)
            pyxel.tri(x + 16, y, x + 2, y + 12, x + 30, y + 12, 13)
            pyxel.rect(x + 14, y + 12, 4, 14, 10)

    def _draw_miniboss(self):
        if self.miniboss is None:
            return

        x = int(self.miniboss.x)
        y = int(self.miniboss.y)
        pyxel.rect(x + 4, y + 8, 40, 14, 2)
        pyxel.tri(x + 24, y + 2, x + 2, y + 14, x + 46, y + 14, 8)
        pyxel.rect(x + 8, y + 18, 32, 6, 5)
        pyxel.rect(x + 20, y + 18, 8, 10, 10)

        hp_w = int((self.miniboss.vidas / 40) * 50)
        pyxel.rect(100, 20, 52, 5, 1)
        pyxel.rect(101, 21, max(0, hp_w), 3, 8)
        pyxel.text(72, 19, "MINI BOSS", 7)

    def _draw_projectiles(self):
        for b in self.misilesavion_list:
            if b.tipo == "laser":
                pyxel.rect(b.x - 1, b.y - 10, 3, 12, 11)
                pyxel.pset(b.x, b.y - 11, 7)
            else:
                pyxel.rect(b.x, b.y - 8, 2, 8, 10)
                pyxel.pset(b.x, b.y - 9, 7)

        for m in self.misilesregular_list:
            pyxel.circ(m.x, m.y, 1, 8)
        for m in self.misilesbombardero_list:
            pyxel.rect(m.x - 1, m.y - 1, 3, 3, 9)
        for m in self.misilesSuperbombardero_list:
            pyxel.rect(m.x - 1, m.y - 1, 3, 3, 14)

    def _draw_perks(self):
        labels = {"double": "D", "rapid": "R", "laser": "L"}
        colors = {"double": 12, "rapid": 11, "laser": 9}

        for perk in self.perks:
            x = int(perk["x"])
            y = int(perk["y"])
            c = colors[perk["type"]]
            pyxel.tri(x, y - 6, x - 6, y, x, y + 6, c)
            pyxel.tri(x, y - 6, x + 6, y, x, y + 6, c)
            pyxel.text(x - 2, y - 2, labels[perk["type"]], 7)

    def _draw_particles(self):
        for p in self.explosion_particles:
            pyxel.pset(p["x"], p["y"], p["color"])

    def _draw_hud(self):
        pyxel.rect(0, 0, self.ancho, 14, 0)
        pyxel.text(5, 4, "SCORE %04d" % self.puntuacion, 7)
        self.recordpuntuacion = max(self.recordpuntuacion, self.puntuacion)
        pyxel.text(84, 4, "HI %04d" % self.recordpuntuacion, 10)
        pyxel.text(150, 4, "DIST %dkm" % (self.distancia // 60), 6)

        for i in range(max(0, self.avion.vidas)):
            base = 205 + i * 16
            pyxel.tri(base + 6, 4, base, 12, base + 12, 12, 8)
            pyxel.rect(base + 5, 10, 2, 3, 10)

        if self.weapon_mode != "normal":
            pyxel.text(5, self.alto - 10, "PERK: %s %02d" % (self.weapon_mode.upper(), self.weapon_timer // 60), 11)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self._update_background()
        self._update_particles()

        if not self.inicio:
            if pyxel.btnp(pyxel.KEY_M):
                self.inicio = True
            return

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_M):
                self._reset_game_state()
                self.inicio = True
            return

        self.distancia += 1

        if self.loop_cooldown > 0:
            self.loop_cooldown -= 1
        if self.fire_timer > 0:
            self.fire_timer -= 1

        if pyxel.btnp(pyxel.KEY_X) and self.loop_cooldown == 0 and self.death_frames == 0:
            if self.avion.iniciar_loop():
                self.loop_cooldown = 90

        self.avion.actualizar_estado(self.ancho)

        if self.death_frames > 0:
            self.death_frames -= 1
            if self.death_frames == 0 and self.pending_respawn and self.avion.vidas > 0:
                self.pending_respawn = False
                self._respawn_player()
        elif not self.avion.rodando:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.avion.mover("derecha", self.ancho)
            if pyxel.btn(pyxel.KEY_LEFT):
                self.avion.mover("izquierda", self.ancho)
            if pyxel.btn(pyxel.KEY_UP):
                self.avion.mover("arriba", self.alto)
            if pyxel.btn(pyxel.KEY_DOWN):
                self.avion.mover("abajo", self.alto)

        if pyxel.btn(pyxel.KEY_SPACE) and self.fire_timer == 0:
            self._fire_player()

        self._update_perks()
        self._spawn_miniboss_if_needed()
        self._spawn_enemies()
        self._update_enemy_logic()

        for b in self.misilesavion_list:
            b.mover()

        self._handle_collisions()

    def draw(self):
        if not self.inicio:
            self._draw_start_screen()
            return

        self._draw_background()

        for enemy in self.regList:
            self._draw_enemy(enemy, "REGULAR")
        for enemy in self.rojoList:
            self._draw_enemy(enemy, "ROJO")
        for enemy in self.bombarderoList:
            self._draw_enemy(enemy, "BOMBARDERO")
        for enemy in self.superBombarderoList:
            self._draw_enemy(enemy, "SUPERBOMBARDERO")

        self._draw_miniboss()
        self._draw_perks()
        self._draw_projectiles()
        self._draw_player()
        self._draw_particles()
        self._draw_hud()

        if self.game_over:
            pyxel.rect(48, 96, 158, 52, 0)
            pyxel.rectb(48, 96, 158, 52, 8)
            pyxel.text(102, 114, "GAME OVER", 8)
            pyxel.text(70, 130, "PULSA M PARA REINTENTAR", 7)
