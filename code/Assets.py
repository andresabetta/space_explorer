#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame

_ASSET_CACHE = {}
_ASSET_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'asset'),
    os.path.join(os.path.dirname(__file__), '..', 'asset'),
    'asset',
]


def _find_asset_path(filename: str):
    for base in _ASSET_DIRS:
        path = os.path.normpath(os.path.join(base, filename))
        if os.path.isfile(path):
            return path
    return None


def load_image(filename: str, size: tuple | None = None, colorkey=None, convert_alpha=True):
    key = (filename, size, colorkey, convert_alpha)
    if key in _ASSET_CACHE:
        return _ASSET_CACHE[key]

    path = _find_asset_path(filename)
    if path is None:
        # fallback: superfície colorida
        surf = pygame.Surface(size or (32, 32), pygame.SRCALPHA)
        surf.fill((200, 0, 200, 255))
        _ASSET_CACHE[key] = surf
        return surf

    image = pygame.image.load(path)
    if convert_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if size is not None:
        image = pygame.transform.smoothscale(image, size)

    if colorkey is not None:
        image.set_colorkey(colorkey)

    _ASSET_CACHE[key] = image
    return image


def get_level_background_images(level_prefix: str):
    # Espera nomes: Level1Bg0.png ... Level1Bg6.png; Level2Bg0.png ...
    images = []
    for i in range(0, 7):
        fname = f"{level_prefix}Bg{i}.png"
        img = load_image(fname, (0, 0))  # tamanho será ajustado no draw
        images.append(img)
    return images


def load_optional(filename: str, size: tuple | None = None):
    path = _find_asset_path(filename)
    if path is None:
        return None
    return load_image(filename, size)
