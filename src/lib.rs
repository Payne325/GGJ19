mod buffer;
mod clock;

use std::{
    thread::sleep,

};
use vek::*;
use minifb::{
    Window,
    WindowOptions,
    Key,
    MouseMode,
};
use image::{
    self,
    RgbaImage,
    DynamicImage,
    GenericImage,
    GenericImageView,
};
use rodio::{
    self,
    Source,
};
use self::buffer::Buffer2d;
use self::clock::Clock;

#[derive(Copy, Clone)]
struct Cell {
    height: f32,
    colour: u32,
    kind: i32,
}

const WHITE: u32 = 0xFFFFFFFF;
const RED: u32   = 0x00FF0000;
const GREEN: u32 = 0x0000FF00;
const BLUE: u32  = 0x000000FF;
const SKY_BLUE: u32  = 0x0080A0FF;
const BROWN: u32   = 0x00FF8000;

impl Cell {
    pub fn new() -> Self {
        Self {
            height: 0.0,
            colour: WHITE,
            kind: 0,
        }
    }
}

struct Player {
    pos: Vec2<f32>,
    ori: f32,
}

impl Player {
    pub fn new() -> Self {
        Self {
            pos: Vec2::new(4.0, 4.0),
            ori: 0.0,
        }
    }

    pub fn move_by(&mut self, dir: Vec2<f32>) {
        // forward/back
        self.pos += Vec2::new(self.ori.cos(), -self.ori.sin()) * dir.x;

        /*
        self.pos_x += cos(ori) * forward_speed
        self.pos_y += -sin(ori) * forward_speed
        */

        // left/right
        let rori = self.ori + std::f32::consts::PI / 4.0;
        self.pos += Vec2::new(rori.cos(), -rori.sin()) * dir.y;
    }

    pub fn get_look_dir(&self, offs: f32) -> Vec2<f32> {
        Vec2::new(
            (self.ori + offs).cos(),
            -(self.ori + offs).sin(),
        )
    }
}

const WORLD_SZ: Vec2<usize> = Vec2 { x: 256, y: 256 };

struct World {
    cells: [[Cell; WORLD_SZ.y]; WORLD_SZ.x],
    player: Player,
}

impl World {
    pub fn new() -> Self {
        let mut world = Self {
            cells: [[Cell::new(); WORLD_SZ.y]; WORLD_SZ.x],
            player: Player::new(),
        };

        for i in 2..32 {
            for j in 2..32 {
                if (i as f32 * 1373.3 + (j as f32 * 2232.3).sin() * 382.7).sin() > 0.95 {
                    world.cells[i][j].height = 1.5;
                    world.cells[i][j].kind = 1;
                }
            }
        }

        /*for i in 0..20 {
            world.cells[0][i].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[0][i].kind = 1;

            world.cells[20][i].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[20][i].kind = 2;

            world.cells[i][0].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[i][0].kind = 3;

            world.cells[i][20].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[i][20].kind = 4;
        }*/

        world
    }

    pub fn get_at(&self, pos: Vec2<usize>) -> &Cell {
        unsafe { self.cells.get_unchecked(pos.x & (WORLD_SZ.x - 1)).get_unchecked(pos.y & (WORLD_SZ.y - 1)) }
    }

    pub fn get_at_mut(&mut self, pos: Vec2<usize>) -> &mut Cell {
        unsafe { self.cells.get_unchecked_mut(pos.x & (WORLD_SZ.x - 1)).get_unchecked_mut(pos.y & (WORLD_SZ.y - 1)) }
    }

    pub fn cast_ray<'a>(&'a self, mut pos: Vec2<f32>, dir: Vec2<f32>, mut t: f32, height_thresh: f32) -> Result<(f32, &'a Cell), ()> {
        const PLANCK: f32 = 0.0001;
        let dir = dir.normalized();
        let step = dir.map(|e| (e.signum() + 1.0).min(1.0));
        for i in 0..128 {
            let cpos = pos + dir * t;

            let cell = self.get_at(cpos.map(|e| e as usize));
            if cell.height > height_thresh {
                return Ok((t, &cell));
            }

            let deltas = (step - cpos.map(|e| e.fract())) / dir;
            t += deltas.reduce_partial_min().max(PLANCK);
        }
        return Err(());
    }
}

struct Textures {
    tiles: RgbaImage,
    floor: RgbaImage,
    wall: RgbaImage,
    sprites: Vec<RgbaImage>,
}

fn rgba_to_u32(p: image::Rgba<u8>) -> u32 {
    (p.data[0] as u32) << 16 |
    (p.data[1] as u32) << 8  |
    (p.data[2] as u32) << 0  |
    (p.data[3] as u32) << 24
}

impl Textures {
    pub fn wall_at(&self, pos: Vec2<f32>, kind: u32) -> u32 {
        let x = ((16.0 * pos.x) as u32) & 0xF;
        let y = ((16.0 * pos.y) as u32) & 0xF;
        unsafe { rgba_to_u32(self.tiles.unsafe_get_pixel(x + kind * 16, y)) }
    }

    pub fn floor_at(&self, pos: Vec2<f32>) -> u32 {
        let x = ((50.0 * pos.x) as u32) & 0xFF;
        let y = ((50.0 * pos.y) as u32) & 0xFF;
        unsafe { rgba_to_u32(self.floor.unsafe_get_pixel(x, y)) }
    }

    pub fn sprite_at(&self, pos: Vec2<f32>, idx: usize) -> u32 {
        let x = (pos.x as u32) & (self.sprite_sz(idx).x - 1);
        let y = (pos.y as u32) & (self.sprite_sz(idx).y - 1);
        unsafe { rgba_to_u32(self.sprites[idx].unsafe_get_pixel(x, y)) }
    }

    pub fn sprite_sz(&self, idx: usize) -> Vec2<u32> {
        Vec2::new(
            self.sprites[idx].width(),
            self.sprites[idx].height(),
        )
    }
}

struct Sounds {
    sounds: Vec<String>,
}

const WIN_SZ: Vec2<usize> = Vec2 { x: 800, y: 600 };

struct Engine {
    clock: Option<Clock>,
    win: Option<Window>,
    music: Option<rodio::Sink>,
    world: Option<World>,
    color: Option<Buffer2d<u32>>,
    depth: Option<Buffer2d<f32>>,
    keys: Option<Vec<i32>>,
    pressed: Option<Vec<i32>>,
    tex: Option<Textures>,
    sound_dev: Option<rodio::Device>,
    sounds: Option<Sounds>,
    //last_mouse_pos: (u32, u32),
}

const FOV: f32 = 0.0011;

fn angle_diff(a: f32, b: f32) -> f32 {
    let pi = std::f32::consts::PI;
    ((((a - b) % (pi * 2.0)) + (pi * 3.0)) % (pi * 2.0)) - (pi * 1.0)
}

impl Engine {
    const fn new() -> Self {
        Self {
            clock: None,
            win: None,
            music: None,
            world: None,
            color: None,
            depth: None,
            keys: None,
            pressed: None,
            tex: None,
            sound_dev: None,
            sounds: None,
            //last_mouse_pos: (0, 0),
        }
    }

    fn close(&mut self) {
        self.clock = None;
        self.win = None;
        self.music = None;
        self.world = None;
        self.color = None;
        self.depth = None;
        self.keys = None;
        self.pressed = None;
        self.tex = None;
        self.sound_dev = None;
        self.sounds = None;
    }

    fn init(&mut self) {
        self.clock = Some(Clock::new());

        self.win = Some(Window::new(
            "GGJ19",
            WIN_SZ.x,
            WIN_SZ.y,
            WindowOptions {
                borderless: false,
                title: true,
                resize: false,
                scale: minifb::Scale::X1,
            },
        ).unwrap());

        self.world = Some(World::new());

        //self.last_mouse_pos = self.win.unwrap().get_mouse_pos(MouseMode::Pass).unwrap();

        self.color = Some(Buffer2d::new(WIN_SZ, 0xFFFFFFFF));
        self.depth = Some(Buffer2d::new(WIN_SZ, 0.0));

        self.keys = Some(vec![]);
        self.pressed = Some(vec![]);

        self.tex = Some(Textures {
            tiles: image::open("assets/tiles.png").unwrap().to_rgba(),
            floor: image::open("assets/floor.png").unwrap().to_rgba(),
            wall: image::open("assets/wall.jpg").unwrap().to_rgba(),
            sprites: vec![
                image::open("assets/zombie.png").unwrap().to_rgba(),
                image::open("assets/mine.png").unwrap().to_rgba(),
                image::open("assets/gun.png").unwrap().to_rgba(),
                image::open("assets/gun-fire.png").unwrap().to_rgba(),
                image::open("assets/heart.png").unwrap().to_rgba(),
                image::open("assets/gun-zoom.png").unwrap().to_rgba(),
                image::open("assets/gun-zoom-fire.png").unwrap().to_rgba(),
                image::open("assets/mine_item.png").unwrap().to_rgba(),
                image::open("assets/health.png").unwrap().to_rgba(),
                image::open("assets/gameover.png").unwrap().to_rgba(),
            ],
        });

        self.sound_dev = Some(rodio::default_output_device().unwrap());

        self.sounds = Some(Sounds {
            sounds: vec![
                String::from("assets/gunshot.wav"), //0
                String::from("assets/mine_pickup.wav"), //1
                String::from("assets/attack.wav"), //2
                String::from("assets/Home_battle1.wav"), //3
                String::from("assets/Footstep_1.wav"), //4
                String::from("assets/Footstep_2.wav"), //5
                String::from("assets/Footstep_3.wav"), //6
                String::from("assets/Footstep_4.wav"), //7
                String::from("assets/home_atmos_1.wav"), //8
                String::from("assets/Gunshot_flesh_1.wav"), //9
                String::from("assets/Gunshot_wall_1.wav"), //10
                String::from("assets/Zombie1.wav"), //11
                String::from("assets/Zombie2.wav"), //12
                String::from("assets/Zombie3.wav"), //13
                String::from("assets/Zombie4.wav"), //14
                String::from("assets/Zombie_death_1.wav"), //15
                String::from("assets/Zombie_death_2.wav"), //16
            ],
        });
    }

    fn draw_world(&mut self) {
        /*
        let mouse_pos = self.win.unwrap().get_mouse_pos(MouseMode::Pass).unwrap();
        self.world.unwrap().player.ori += (mouse_pos.0 - self.last_mouse_pos.0) * 0.02;
        self.last_mouse_pos = mouse_pos;
        */

        let mut color = self.color.as_mut().unwrap();
        let mut depth = self.depth.as_mut().unwrap();
        let mut world = self.world.as_mut().unwrap();
        let mut win = self.win.as_mut().unwrap();
        let mut tex = self.tex.as_mut().unwrap();

        // Render
        const RED_BROWN: u32 = 0xFF804000;
        //color.clear(RED_BROWN);
        depth.clear(10000.0);

        let floor_dists = (WIN_SZ.y / 2..WIN_SZ.y)
            .map(|y| (std::f32::consts::PI / 2.0 - (y as f32 - WIN_SZ.y as f32 / 2.0) * 0.002).tan())
            .collect::<Vec<_>>();

        for x in 0..WIN_SZ.x {
            let col_dir = world.player
                .get_look_dir((x as f32 - WIN_SZ.x as f32 / 2.0) * FOV);

            for y in 0..WIN_SZ.y / 2 {
                let dist = floor_dists[y];// + (y as f32).sin().sin().sin().sin().sin().sin().sin().sin().sin().sin().sin().sin().sin() * 0.0001;
                color.set(Vec2::new(x, y + WIN_SZ.y / 2), tex.floor_at(world.player.pos + col_dir * dist));
                color.set(Vec2::new(x, WIN_SZ.y / 2 - y), tex.floor_at(world.player.pos + col_dir * dist));
                depth.set(Vec2::new(x, y + WIN_SZ.y / 2), dist);
                depth.set(Vec2::new(x, WIN_SZ.y / 2 - y), dist);
            }

            let mut lim_min = WIN_SZ.y;
            let mut height_thresh = 0.0;
            let mut t = 0.0;
            for i in 0..3 {
                if let Ok((dist, cell)) = world.cast_ray(world.player.pos, col_dir, t, height_thresh) {
                    let top_height = 1000.0 * (cell.height - 0.5).atan2(dist);
                    let bot_height = 1000.0 * (0.5f32).atan2(dist);
                    let base = (WIN_SZ.y as f32 / 2.0 - top_height);
                    let lim = (WIN_SZ.y / 2 + bot_height as usize);

                    let cpos = world.player.pos + col_dir * dist;
                    let tex_x = cpos.sum().fract();

                    for y in base.max(0.0) as usize..lim.min(WIN_SZ.y).min(lim_min) {
                        let yfract = (y - base as usize) as f32 / (lim - base as usize) as f32;
                        let pix = tex.wall_at(Vec2::new(tex_x, yfract), cell.kind as u32);
                        color.set(Vec2::new(x, y), pix);
                        depth.set(Vec2::new(x, y), dist);
                    }
                    if (base.max(0.0) as usize) < lim_min {
                        lim_min = base.max(0.0) as usize;
                        height_thresh = cell.height;
                    }
                    t = dist;
                }
            }
        }

        //draw_sprite(6.0, 6.0, (world.player.pos - Vec2::broadcast(6.0)).magnitude(), 0);
        //draw_sprite(15.0, 15.0, (world.player.pos - Vec2::broadcast(15.0)).magnitude(), 1);

        //draw_decal(128, 128, 0);

        let mut keys = vec![];
        for key in win.get_keys().unwrap_or(vec![]) {
            match key {
                Key::W => keys.push(0),
                Key::A => keys.push(1),
                Key::S => keys.push(2),
                Key::D => keys.push(3),
                Key::Left => keys.push(4),
                Key::Right => keys.push(5),
                Key::Space => keys.push(6),
                Key::LeftShift => keys.push(7),
                _ => {},
            }
        }
        self.keys = Some(keys);

        let mut pressed = vec![];
        for key in win.get_keys_pressed(minifb::KeyRepeat::No).unwrap_or(vec![]) {
            match key {
                Key::Q => pressed.push(0),
                Key::E => pressed.push(1),
                _ => {},
            }
        }
        self.pressed = Some(pressed);
    }

    fn draw_sprite(&mut self, pos: Vec2<f32>, dist: f32, img: i32) {
        let mut color = self.color.as_mut().unwrap();
        let mut depth = self.depth.as_mut().unwrap();
        let mut world = self.world.as_mut().unwrap();
        let mut win = self.win.as_mut().unwrap();
        let mut tex = self.tex.as_mut().unwrap();

        for x in 0..WIN_SZ.x {
            let scrn_ori = world.player.ori + (x as f32 - WIN_SZ.x as f32 / 2.0) * FOV;

            let rpos = (pos - world.player.pos).normalized();
            let scrn_img_ori = (-rpos.y).atan2(rpos.x);

            let rori = angle_diff(scrn_ori, scrn_img_ori);
            let xx = rori * 100.0 * dist * 1.5 + 64.0;

            if xx < 0.0 || xx > 128.0 {
                continue;
            }
            for y in 0..WIN_SZ.y {
                let rpos = Vec2::new(
                    xx,
                    (y as f32 - WIN_SZ.y as f32 / 2.0) * 1.5 * 0.15 * dist + 24.0,
                );
                if rpos.y > 0.0 {
                    if dist < *depth.get(Vec2::new(x, y)) {
                        let px = tex.sprite_at(rpos, img as usize);
                        if px & 0xFF000000 != 0 {
                            color.set(Vec2::new(x, y), px);
                            depth.set(Vec2::new(x, y), dist);
                        }
                    }
                }
            }
        }
    }

    fn draw_decal(&mut self, pos: Vec2<u32>, img: i32) {
        let mut color = self.color.as_mut().unwrap();
        let mut world = self.world.as_mut().unwrap();
        let mut win = self.win.as_mut().unwrap();
        let mut tex = self.tex.as_mut().unwrap();

        let sz = tex.sprite_sz(img as usize);

        for x in pos.x as usize..(pos.x as usize + sz.x as usize).min(WIN_SZ.x) {
            for y in pos.y as usize..(pos.y as usize + sz.y as usize).min(WIN_SZ.y) {
                let px = tex.sprite_at(Vec2::new((x - pos.x as usize) as f32, (y - pos.y as usize) as f32), img as usize);
                if px & 0xFF000000 != 0 {
                    color.set(Vec2::new(x, y), px);
                }
            }
        }
    }

    pub fn update_window(&mut self) -> f32 {
        let mut color = self.color.as_mut().unwrap();
        let mut win = self.win.as_mut().unwrap();
        win.update_with_buffer(color.as_ref()).unwrap();

        self.clock.as_mut().unwrap().tick(std::time::Duration::from_millis(1000 / 60));
        (1000.0 / 60.0) / self.clock.as_mut().unwrap().get_last_delta().subsec_millis() as f32
    }
}

unsafe impl Sync for Engine {}

static mut ENGINE: Engine = Engine::new();

#[no_mangle]
pub extern "C" fn init_engine() {
    let mut engine = unsafe { &mut ENGINE };
    *engine = Engine::new();
    engine.init();
}

#[no_mangle]
pub extern "C" fn close_engine() {
    let mut engine = unsafe { &mut ENGINE };
    engine.close();
}

#[no_mangle]
pub extern "C" fn window_is_open() -> i32 {
    let engine = unsafe { &mut ENGINE };
    if engine.win.as_mut().unwrap().is_open() { 1 } else { 0 }
}

#[no_mangle]
pub extern "C" fn draw_world() {
    let mut engine = unsafe { &mut ENGINE };
    engine.draw_world();
}

#[no_mangle]
pub extern "C" fn update_window() -> f32 {
    let mut engine = unsafe { &mut ENGINE };
    engine.update_window()
}

#[no_mangle]
pub extern "C" fn get_key(code: i32) -> i32 {
    let mut engine = unsafe { &mut ENGINE };
    if engine.keys.as_mut().unwrap().contains(&code) { 1 } else { 0 }
}

#[no_mangle]
pub extern "C" fn get_key_pressed(code: i32) -> i32 {
    let mut engine = unsafe { &mut ENGINE };
    if engine.pressed.as_mut().unwrap().contains(&code) { 1 } else { 0 }
}

#[no_mangle]
pub extern "C" fn put_camera(x: f32, y: f32, ori: f32) {
    let mut engine = unsafe { &mut ENGINE };
    engine.world.as_mut().unwrap().player.pos = Vec2::new(x, y);
    engine.world.as_mut().unwrap().player.ori = ori;
}

#[no_mangle]
pub extern "C" fn set_cell(x: i32, y: i32, height: f32, kind: i32) {
    let mut engine = unsafe { &mut ENGINE };
    engine.world.as_mut().unwrap().get_at_mut(Vec2::new(x as usize, y as usize)).height = height;
    engine.world.as_mut().unwrap().get_at_mut(Vec2::new(x as usize, y as usize)).kind = kind;
}

#[no_mangle]
pub extern "C" fn get_cell_height(x: i32, y: i32) -> f32 {
    let mut engine = unsafe { &mut ENGINE };
    engine.world.as_mut().unwrap().get_at_mut(Vec2::new(x as usize, y as usize)).height
}

#[no_mangle]
pub extern "C" fn get_cell_kind(x: i32, y: i32) -> i32 {
    let mut engine = unsafe { &mut ENGINE };
    engine.world.as_mut().unwrap().get_at_mut(Vec2::new(x as usize, y as usize)).kind
}

#[no_mangle]
pub extern "C" fn play_sound(n: i32) {
    let mut engine = unsafe { &mut ENGINE };
    let mut sound_dev = engine.sound_dev.as_mut().unwrap();
    let mut sounds = engine.sounds.as_mut().unwrap();

    rodio::play_once(sound_dev, std::io::BufReader::new(std::fs::File::open(&sounds.sounds[n as usize]).unwrap())).unwrap().detach();
}

#[no_mangle]
pub extern "C" fn play_music(n: i32) {
    let mut engine = unsafe { &mut ENGINE };
    let mut sound_dev = engine.sound_dev.as_mut().unwrap();
    let mut sounds = engine.sounds.as_mut().unwrap();

    engine.music = Some(rodio::play_once(sound_dev, std::io::BufReader::new(std::fs::File::open(&sounds.sounds[n as usize]).unwrap())).unwrap());
    engine.music.as_mut().unwrap().set_volume(0.4);
}

#[no_mangle]
pub extern "C" fn music_is_playing() -> i32 {
    let mut engine = unsafe { &mut ENGINE };

    if engine.music.as_ref().map(|snd| !snd.empty()).unwrap_or(false) { 1 } else { 0 }
}

#[no_mangle]
pub extern "C" fn draw_sprite(x: f32, y: f32, dist: f32, img: i32) {
    let mut engine = unsafe { &mut ENGINE };
    engine.draw_sprite(Vec2::new(x, y), dist, img);
}

#[no_mangle]
pub extern "C" fn draw_billboard(x: f32, y: f32, img: i32) {
    let mut engine = unsafe { &mut ENGINE };
    let dist = engine.world.as_mut().unwrap().player.pos.distance(Vec2::new(x, y));
    engine.draw_sprite(Vec2::new(x, y), dist, img);
}

#[no_mangle]
pub extern "C" fn draw_decal(x: i32, y: i32, img: i32) {
    let mut engine = unsafe { &mut ENGINE };
    engine.draw_decal(Vec2::new(x as u32, y as u32), img);
}

#[no_mangle]
pub extern "C" fn cast_ray(x: f32, y: f32, dir_x: f32, dir_y: f32, min_height: f32) -> i32 {
    let mut engine = unsafe { &mut ENGINE };
    engine.world.as_mut().unwrap().cast_ray(Vec2::new(x, y), Vec2::new(dir_x, dir_y), 0.0, min_height).map(|e| e.0 * 100.0).unwrap_or(100000.0) as i32
}
