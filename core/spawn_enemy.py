from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union
import pygame

from entities.enemies import (
    Mizuaka, MizuakaZigZag, MizuakaZigZagInversed, MizuakaRightMover,
    MizuakaShooter, MizuakaFormation, MizuakaDownLeftMover, MizuakaUpLeftMover,
    MizuakaDirectedMover, MizuakaCircleTrap,
    Abura, AburaSlow, AburaFormation, AburaRight, AburaUp, AburaDown,
    AburaStopShooter, AburaCurveCharger,
    Sabi, SabiInversed, SabiPlus, SabiOrbit, SabiBind, SabiFormation,
    SabiCharger, SabiChargerInversed,
    Kabi, KabiFormation, KabiDownMover, KabiUpMover, KabiRight,
)

@dataclass
class SpawnContext:
    enemy_type: str
    x_pos: int
    y_pos: int
    IMG: Dict[str, pygame.Surface]
    all_sprites: pygame.sprite.Group
    enemies: pygame.sprite.Group
    gm: Any
    fragment_group: pygame.sprite.Group
    fragment_image: pygame.Surface
    extra_groups: Optional[Dict[str, pygame.sprite.Group]] = None
    player: Optional[Any] = None
    speed: Optional[float] = None
    x_speed_factor: Optional[float] = None
    enemy_data: Optional[Dict[str, Any]] = None
    bullet_group: Optional[pygame.sprite.Group] = None


def _common_setup(inst: pygame.sprite.Sprite, ctx: SpawnContext) -> None:
    if hasattr(inst, 'rect'):
        inst.rect.x = ctx.x_pos
        inst.rect.y = ctx.y_pos
    if ctx.speed is not None and hasattr(inst, 'speed'):
        inst.speed = ctx.speed
    inst.fragment_group = ctx.fragment_group
    inst.fragment_image = ctx.fragment_image
    inst.gm = ctx.gm
    ctx.all_sprites.add(inst)
    ctx.enemies.add(inst)
    if hasattr(inst, 'members'):
        for member in inst.members:
            member.fragment_group = ctx.fragment_group
            member.fragment_image = ctx.fragment_image
            member.gm = ctx.gm

Factory = Callable[[SpawnContext], Union[pygame.sprite.Sprite, List[pygame.sprite.Sprite]]]
ENEMY_FACTORY: Dict[str, Factory] = {}

def register(name: str) -> Callable[[Factory], Factory]:
    def decorator(func: Factory) -> Factory:
        ENEMY_FACTORY[name] = func
        return func
    return decorator

# Mizuaka
@register("Mizuaka")
def _create_mizuaka(ctx: SpawnContext):
    return Mizuaka(ctx.IMG["mizuaka"])

@register("MizuakaZigZag")
def _create_mizuaka_zigzag(ctx: SpawnContext):
    return MizuakaZigZag(ctx.IMG["mizuaka"], ctx.all_sprites, ctx.enemies, ctx.speed)

@register("MizuakaZigZagInversed")
def _create_mizuaka_zigzag_inv(ctx: SpawnContext):
    return MizuakaZigZagInversed(ctx.IMG["mizuaka"], ctx.all_sprites, ctx.enemies, ctx.speed)

@register("MizuakaRightMover")
def _create_mizuaka_right(ctx: SpawnContext):
    return MizuakaRightMover(ctx.IMG["mizuaka"], ctx.all_sprites, ctx.enemies, ctx.speed)

@register("MizuakaShooter")
def _create_mizuaka_shooter(ctx: SpawnContext):
    return MizuakaShooter(ctx.IMG["mizuaka"], ctx.player, ctx.extra_groups.get("mizuaka_bullets"), ctx.all_sprites)

@register("MizuakaFormation")
def _create_mizuaka_formation(ctx: SpawnContext):
    return MizuakaFormation(ctx.IMG["mizuaka"], ctx.all_sprites, ctx.enemies)

@register("MizuakaUpLeftMover")
def _create_mizuaka_up_left(ctx: SpawnContext):
    return MizuakaUpLeftMover(ctx.IMG["mizuaka"], ctx.x_pos, ctx.y_pos, ctx.speed, ctx.x_speed_factor)

@register("MizuakaDownLeftMover")
def _create_mizuaka_down_left(ctx: SpawnContext):
    return MizuakaDownLeftMover(ctx.IMG["mizuaka"], ctx.x_pos, ctx.y_pos, ctx.speed, ctx.x_speed_factor)

@register("MizuakaRotationSpawner")
def _create_mizuaka_rotation(ctx: SpawnContext):
    return MizuakaDirectedMover(
        ctx.IMG["mizuaka"], ctx.x_pos, ctx.y_pos, ctx.speed,
        target_pos=(600, 400), gm=ctx.gm,
        fragment_image=ctx.fragment_image, fragment_group=ctx.fragment_group
    )

@register("MizuakaCircleTrapBatch")
def _create_mizuaka_circle_batch(ctx: SpawnContext):
    cfg = ctx.enemy_data or {}
    cx, cy = cfg.get("center_x", 600), cfg.get("center_y", 400)
    num, spd = cfg.get("num", 12), cfg.get("speed", 5)
    traps: List[pygame.sprite.Sprite] = []
    step = 360 / num
    for i in range(num):
        angle = i * step
        traps.append(
            MizuakaCircleTrap(
                ctx.IMG["mizuaka"], angle, (cx, cy), spd,
                gm=ctx.gm,
                fragment_image=ctx.fragment_image,
                fragment_group=ctx.fragment_group
            )
        )
    return traps

# Abura
@register("Abura")
def _create_abura(ctx: SpawnContext):
    return Abura(
        ctx.IMG["abura"],
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

@register("AburaRight")
def _create_abura_right(ctx: SpawnContext):
    return AburaRight(
        ctx.IMG["abura"],
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

@register("AburaUp")
def _create_abura_up(ctx: SpawnContext):
    return AburaUp(
        ctx.IMG["abura"],
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

@register("AburaDown")
def _create_abura_down(ctx: SpawnContext):
    return AburaDown(
        ctx.IMG["abura"],
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

@register("AburaSlow")
def _create_abura_slow(ctx: SpawnContext):
    return AburaSlow(
        ctx.IMG["abura"], ctx.all_sprites, ctx.extra_groups.get("slow_bullets"),
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

@register("AburaStopShooter")
def _create_abura_stop(ctx: SpawnContext):
    return AburaStopShooter(
        ctx.IMG["abura"], ctx.all_sprites, ctx.extra_groups.get("slow_bullets"), ctx.player,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

@register("AburaFormation")
def _create_abura_formation(ctx: SpawnContext):
    return AburaFormation(
        ctx.IMG["abura"], ctx.all_sprites, ctx.enemies,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

@register("AburaCurveCharger")
def _create_abura_curve(ctx: SpawnContext):
    return AburaCurveCharger(
        ctx.IMG["abura"], ctx.player, ctx.all_sprites, ctx.enemies,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group,
        gm=ctx.gm
    )

# Sabi
@register("Sabi")
def _create_sabi(ctx: SpawnContext):
    return Sabi(
        ctx.IMG["sabi"], dy=0, can_split=True,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("SabiInversed")
def _create_sabi_inv(ctx: SpawnContext):
    return SabiInversed(
        ctx.IMG["sabi"], dy=0, can_split=True,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("SabiPlus")
def _create_sabi_plus(ctx: SpawnContext):
    return SabiPlus(
        ctx.IMG["sabi"], dy=0, can_split=True,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("SabiOrbit")
def _create_sabi_orbit(ctx: SpawnContext):
    return SabiOrbit(
        ctx.IMG["sabi"], dy=0, can_split=True,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("SabiBind")
def _create_sabi_bind(ctx: SpawnContext):
    return SabiBind(
        ctx.IMG["sabi"], dy=0, can_split=True,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("SabiFormation")
def _create_sabi_formation(ctx: SpawnContext):
    return SabiFormation(
        image_surface=ctx.IMG["sabi"], all_sprites=ctx.all_sprites, enemies_group=ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("SabiCharger")
def _create_sabi_charger(ctx: SpawnContext):
    return SabiCharger(
        ctx.IMG["sabi"], player=ctx.player, all_sprites=ctx.all_sprites, enemies_group=ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("SabiChargerInversed")
def _create_sabi_charger_inv(ctx: SpawnContext):
    return SabiChargerInversed(
        ctx.IMG["sabi"], player=ctx.player, all_sprites=ctx.all_sprites, enemies_group=ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

# Kabi
@register("Kabi")
def _create_kabi(ctx: SpawnContext):
    return Kabi(
        ctx.IMG["kabi"], ctx.IMG.get("kabismoke"), ctx.all_sprites, ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("KabiRight")
def _create_kabi_right(ctx: SpawnContext):
    return KabiRight(
        ctx.IMG["kabi"], ctx.IMG.get("kabismoke"), ctx.all_sprites, ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("KabiFormation")
def _create_kabi_formation(ctx: SpawnContext):
    return KabiFormation(
        ctx.IMG["kabi"], ctx.all_sprites, ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("KabiDownMover")
def _create_kabi_down(ctx: SpawnContext):
    return KabiDownMover(
        ctx.IMG["kabi"], ctx.IMG.get("kabismoke"), ctx.all_sprites, ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

@register("KabiUpMover")
def _create_kabi_up(ctx: SpawnContext):
    return KabiUpMover(
        ctx.IMG["kabi"], ctx.IMG.get("kabismoke"), ctx.all_sprites, ctx.enemies,
        gm=ctx.gm,
        fragment_image=ctx.fragment_image,
        fragment_group=ctx.fragment_group
    )

# Boss
@register("Boss")
def _create_boss(ctx: SpawnContext):
    if ctx.bullet_group is None:
        raise ValueError("Boss.bullet_group is None.")
    from entities.enemies.boss import Boss
    return Boss(
        ctx.IMG["boss"], ctx.gm.stage_controller.spawn_enemy_func,
        ctx.bullet_group, ctx.all_sprites, gm=ctx.gm
    )


def spawn_enemy(
    enemy_type: str,
    x_pos: int,
    y_pos: int,
    IMG: Dict[str, pygame.Surface],
    all_sprites: pygame.sprite.Group,
    enemies: pygame.sprite.Group,
    gm: Any,
    fragment_group: pygame.sprite.Group,
    fragment_image: pygame.Surface,
    extra_groups: Optional[Dict[str, pygame.sprite.Group]] = None,
    player: Optional[Any] = None,
    speed: Optional[float] = None,
    x_speed_factor: Optional[float] = None,
    enemy_data: Optional[Dict[str, Any]] = None,
    bullet_group: Optional[pygame.sprite.Group] = None,
) -> None:
    ctx = SpawnContext(
        enemy_type, x_pos, y_pos, IMG, all_sprites, enemies, gm,
        fragment_group, fragment_image, extra_groups,
        player, speed, x_speed_factor, enemy_data, bullet_group
    )
    factory = ENEMY_FACTORY.get(enemy_type)
    if factory is None:
        raise ValueError(f"Unknown enemy type: {enemy_type}")
    result = factory(ctx)
    instances = result if isinstance(result, list) else [result]
    for inst in instances:
        _common_setup(inst, ctx)
