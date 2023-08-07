import pygame

class Button():
	def __init__(self, x, y, image, image_press, scale, offset):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.image_press = pygame.transform.scale(image_press, (int(width * scale), int(height * scale)))
		self.offset = offset
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		real_pos_x = pos[0] - self.offset

		#check mouseover and clicked conditions
		if self.rect.collidepoint((real_pos_x, pos[1])):
			surface.blit(self.image_press, (self.rect.x, self.rect.y))
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action

class CheckBox():
	def __init__(self, x, y, image, image_press, image_tick, image_tick_press, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.image_press = pygame.transform.scale(image_press, (int(width * scale), int(height * scale)))
		self.image_tick = pygame.transform.scale(image_tick, (int(width * scale), int(height * scale)))
		self.image_tick_press = pygame.transform.scale(image_tick_press, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.checked = False

	def draw(self, surface):
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions for unticked
		if not self.checked:
			if self.rect.collidepoint(pos):
				surface.blit(self.image_press, (self.rect.x, self.rect.y))
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					self.checked = True
			else:
				surface.blit(self.image, (self.rect.x, self.rect.y))
		else:
			#check mouseover and clicked conditions for ticked
			if self.rect.collidepoint(pos) and self.checked:
				surface.blit(self.image_tick_press, (self.rect.x, self.rect.y))
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					self.checked = False
			else:
				surface.blit(self.image_tick, (self.rect.x, self.rect.y))

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return self.checked
