// Program creates ppm image from given pixels data

use std::fs::File;
use std::io;
use std::io::Write;

fn save_as_ppm(file_path: &str, pixels: &[u32], height: usize, width: usize) -> io::Result<()>
{
    let mut file = File::create(file_path)?;
    write!(file, "P6\n{} {} 255\n", width, height);
    for y in 0..width
    {
        for x in 0..height
        {
            let pixel = pixels[y * width + x];
            let color = [((pixel >> 16) & 0xFF) as u8,
                            ((pixel >> 8) & 0xFF) as u8,
                            (pixel & 0xFF) as u8
            ];
            print!("{:?}", color);
            file.write(&color)?;
        }
    }
    Ok(())
}

fn main()
{
    const WIDTH: usize = 64;
    const HEIGHT: usize = 64;
    const OUTPUT_PATH: &str = "output.ppm";
    let mut pixels = [0u32; WIDTH * HEIGHT];
    pixels.fill(0xFFFFFF);
    pixels[0] = 0x000010;
    pixels[1] = 0x000010;
    pixels[2] = 0x000010;
    pixels[3] = 0x000010;
    pixels[4] = 0x000010;
    pixels[5] = 0x000012;
    pixels[6] = 0x100010;
    pixels[7] = 0x011100;
    pixels[8] = 0x000000;
    pixels[9] = 0x000000;
    save_as_ppm(OUTPUT_PATH, &pixels, HEIGHT, WIDTH);
}
