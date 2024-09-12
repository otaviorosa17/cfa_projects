from machine import Pin, I2C
import ssd1306
import framebuf

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Use the correct GPIO pins

# Initialize the OLED display
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # Adjust width and height if needed

# Create a frame buffer
buf = bytearray(128 * 64 // 8)  # Buffer size for a 128x64 display
fb = framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_HLSB)

def Clear():
    oled.fill(0)
    oled.show()

def Dinheiro(icon):

    # Clear the display
    oled.fill(0)

    # Draw the icon
    # Adjust the dimensions and coordinates as necessary
    icon_width = 32
    icon_height = 32
    display_width = 128
    display_height = 64
    x_pos = (display_width - icon_width) // 2
    y_pos = (display_height - icon_height) // 2
    fb.blit(framebuf.FrameBuffer(icon, icon_width, icon_height, framebuf.MONO_HLSB), x_pos, y_pos)

    # Display the content
    oled.blit(framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_HLSB), 0, 0)
    oled.show()

