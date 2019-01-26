use vek::*;

pub struct Buffer2d<T> {
    items: Vec<T>,
    size: Vec2<usize>,
}

impl<T: Clone> Buffer2d<T> {
    pub fn new(size: Vec2<usize>, fill: T) -> Self {
        Self {
            items: vec![fill; size.x * size.y],
            size,
        }
    }

    #[inline(always)]
    fn size(&self) -> Vec2<usize> {
        self.size
    }

    #[inline(always)]
    pub fn set(&mut self, pos: Vec2<usize>, item: T) {
        *unsafe { self.items.get_unchecked_mut(pos.y * self.size.x + pos.x) } = item;
    }

    #[inline(always)]
    pub fn get(&self, pos: Vec2<usize>) -> &T {
        unsafe { self.items.get_unchecked(pos.y * self.size.x + pos.x) }
    }

    pub fn clear(&mut self, fill: T) {
        self.items = vec![fill; self.size.x * self.size.y];
    }
}

impl<T> AsRef<[T]> for Buffer2d<T> {
    fn as_ref(&self) -> &[T] {
        &self.items
    }
}
