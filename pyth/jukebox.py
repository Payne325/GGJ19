class Jukebox:
  def __init__(self, engine):
    self.music = [3, 8]
    self.engine = engine
    self.jbIndex = 0

  def IsPlaying(self):
    return self.engine.music_is_playing() == 1

  def PlayMusic(self):
    if self.IsPlaying() == False:
      self.engine.play_music(self.music[self.jbIndex])
      self.jbIndex += 1
      if self.jbIndex == 2:
        self.jbIndex = 0
