#!/usr/bin/env python3
import pygame
import sys

try:
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("テスト")
    print("Pygame initialized successfully")
    print("Display mode:", pygame.display.get_surface().get_size())
    
    # Quick test
    screen.fill((255, 255, 255))
    pygame.display.flip()
    
    pygame.time.wait(2000)  # Wait 2 seconds
    pygame.quit()
    print("Display test completed")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)