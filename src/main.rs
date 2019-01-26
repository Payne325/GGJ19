mod buffer;

use std::thread::sleep;
use vek::*;
use minifb::{
    Window,
    WindowOptions,
    Key,
    MouseMode,
};
use self::buffer::Buffer2d;

#[derive(Copy, Clone)]
struct Cell {
    height: f32,
    colour: u32,
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
            pos: Vec2::zero(),
            ori: 0.0,
        }
    }

    pub fn move_by(&mut self, dir: Vec2<f32>) {
        self.pos += Vec2::new(self.ori.cos(), -self.ori.sin()) * dir.x;
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

const WORLD_SZ: Vec2<usize> = Vec2 { x: 64, y: 64 };

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

        for i in 0..20 {
            let col = if i % 2 == 0 {
                RED
            } else {
                BLUE
            };

            world.cells[0][i].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[0][i].colour = col;

            world.cells[20][i].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[20][i].colour = col;

            world.cells[i][0].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[i][0].colour = col;

            world.cells[i][20].height = 0.7 + (i % 4) as f32 * 0.25;
            world.cells[i][20].colour = col;
        }

        world
    }

    pub fn get_at(&self, pos: Vec2<usize>) -> Option<&Cell> {
        self.cells.get(pos.x).and_then(|col| col.get(pos.y))
    }

    pub fn cast_ray<'a>(&'a self, mut pos: Vec2<f32>, dir: Vec2<f32>, mut t: f32, height_thresh: f32) -> Result<(f32, &'a Cell), ()> {
        const PLANCK: f32 = 0.0001;
        for i in 0..100 {
            let cpos = pos + dir * t;

            if let Some(cell) = self.get_at(cpos.map(|e| e as usize)) {
                if cell.height > height_thresh {
                    return Ok((t, &cell));
                }
            }

            let deltas = (dir.map(|e| (e.signum() + 1.0).min(1.0)) - cpos.map(|e| e.fract())) / dir;
            t += deltas.reduce_partial_min().max(PLANCK);
        }
        return Err(());
    }
}

const WIN_SZ: Vec2<usize> = Vec2 { x: 800, y: 600 };

fn main() {
    let mut win = Window::new(
        "GGJ19",
        WIN_SZ.x,
        WIN_SZ.y,
        WindowOptions::default(),
    ).unwrap();

    let mut color = Buffer2d::new(WIN_SZ, 0xFFFFFFFF);

    let mut world = World::new();

    let mut last_mouse_pos = win.get_mouse_pos(MouseMode::Pass).unwrap();

    while win.is_open() {
        let mouse_pos = win.get_mouse_pos(MouseMode::Pass).unwrap();
        world.player.ori += (mouse_pos.0 - last_mouse_pos.0) * 0.02;
        last_mouse_pos = mouse_pos;

        // Input
        for key in win.get_keys().unwrap_or(vec![]) {
            match key {
                Key::W => world.player.move_by(Vec2::new( 0.05,  0.0)),
                Key::A => world.player.move_by(Vec2::new( 0.0, -0.05)),
                Key::D => world.player.move_by(Vec2::new( 0.0,  0.05)),
                Key::S => world.player.move_by(Vec2::new(-0.05,  0.0)),
                Key::Left => world.player.ori -= 0.04,
                Key::Right => world.player.ori += 0.04,
                _ => {},
            }
        }

        // Render
        color.clear(SKY_BLUE);

        for x in 0..WIN_SZ.x {
            for y in WIN_SZ.y / 2..WIN_SZ.y {
                color.set(Vec2::new(x, y), BROWN);
            }
        }

        for x in 0..WIN_SZ.x {
            const FOV: f32 = 0.0015;
            let col_dir = world.player
                .get_look_dir((x as f32 - WIN_SZ.x as f32 / 2.0) * FOV);


            let mut lim_min = WIN_SZ.y;
            let mut height_thresh = 0.0;
            let mut t = 0.0;
            for i in 0..10 {
                if let Ok((dist, cell)) = world.cast_ray(world.player.pos, col_dir, t, height_thresh) {
                    let top_height = 1000.0 * (cell.height - 0.5).atan2(dist);
                    let bot_height = 1000.0 * (0.5f32).atan2(dist);
                    let base = (WIN_SZ.y as f32 / 2.0 - top_height).max(0.0) as usize;
                    let lim = (WIN_SZ.y / 2 + bot_height as usize).min(WIN_SZ.y);
                    for y in base..lim.min(lim_min) {
                        color.set(Vec2::new(x, y), cell.colour);
                    }
                    if (lim < lim_min) {
                        lim_min = base;
                        height_thresh = cell.height;
                    }
                    t = dist;
                }
            }
        }

        win.update_with_buffer(color.as_ref()).unwrap();
    }
}
