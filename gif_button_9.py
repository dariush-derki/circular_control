import tkinter as tk
from PIL import Image, ImageTk
import winsound
import os
import math


# =========================================================
# SETTINGS
# =========================================================

GIF1 = "1.gif"
GIF2 = "2.gif"
GIF3 = "3.gif"

WINDOW_SIZE = 600

GIF3_SIZE = 180
# دکمه‌های اطراف
GIF_SIZE = 90

# گیف وسط
CENTER_GIF_SIZE = 400

# فاصله دکمه‌های اطراف از مرکز
BUTTON_RADIUS = 205

# مدت نمایش GIF3 هنگام کلیک
CLICK_GIF_TIME = 450

# رنگ‌ها
BG_COLOR = "#080808"
TRANSPARENT_COLOR = "#00ff00"

DRAG_THRESHOLD = 8


# =========================================================
# ROOT WINDOW
# =========================================================

root = tk.Tk()
root.title("Circular Control")

root.overrideredirect(True)
root.resizable(False, False)

root.configure(bg=TRANSPARENT_COLOR)

try:
    root.wm_attributes(
        "-transparentcolor",
        TRANSPARENT_COLOR
    )
except:
    pass


# =========================================================
# CENTER WINDOW ON SCREEN
# =========================================================

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

pos_x = (screen_width - WINDOW_SIZE) // 2
pos_y = (screen_height - WINDOW_SIZE) // 2

root.geometry(
    f"{WINDOW_SIZE}x{WINDOW_SIZE}+{pos_x}+{pos_y}"
)


# =========================================================
# WINDOW DRAG
# =========================================================

dragging = False

drag_start_mouse_x = 0
drag_start_mouse_y = 0

drag_start_window_x = 0
drag_start_window_y = 0


def start_window_drag(event):

    global dragging
    global drag_start_mouse_x
    global drag_start_mouse_y
    global drag_start_window_x
    global drag_start_window_y

    dragging = False

    drag_start_mouse_x = event.x_root
    drag_start_mouse_y = event.y_root

    drag_start_window_x = root.winfo_x()
    drag_start_window_y = root.winfo_y()


def move_window(event):

    global dragging

    dx = event.x_root - drag_start_mouse_x
    dy = event.y_root - drag_start_mouse_y

    if (
        abs(dx) > DRAG_THRESHOLD
        or
        abs(dy) > DRAG_THRESHOLD
    ):
        dragging = True

    if dragging:

        new_x = drag_start_window_x + dx
        new_y = drag_start_window_y + dy

        root.geometry(
            f"+{new_x}+{new_y}"
        )


def stop_window_drag(event):

    global dragging

    dragging = False


# =========================================================
# ROOT DRAG EVENTS
# =========================================================

root.bind(
    "<ButtonPress-1>",
    start_window_drag
)

root.bind(
    "<B1-Motion>",
    move_window
)

root.bind(
    "<ButtonRelease-1>",
    stop_window_drag
)

root.bind(
    "<ButtonPress-2>",
    start_window_drag
)

root.bind(
    "<B2-Motion>",
    move_window
)

root.bind(
    "<ButtonRelease-2>",
    stop_window_drag
)

root.bind(
    "<Alt-ButtonPress-1>",
    start_window_drag
)

root.bind(
    "<Alt-B1-Motion>",
    move_window
)

root.bind(
    "<Alt-ButtonRelease-1>",
    stop_window_drag
)

root.bind(
    "<Escape>",
    lambda e: root.destroy()
)


# =========================================================
# LOAD GIF
# =========================================================

def load_gif(path, size):

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"GIF پیدا نشد:\n{os.path.abspath(path)}"
        )

    gif = Image.open(path)

    frames = []

    for i in range(gif.n_frames):

        gif.seek(i)

        frame = gif.convert("RGBA")

        # حفظ نسبت تصویر
        frame.thumbnail(
            (size, size),
            Image.Resampling.LANCZOS
        )

        # قاب شفاف
        frame_canvas = Image.new(
            "RGBA",
            (size, size),
            (0, 0, 0, 0)
        )

        x = (size - frame.width) // 2
        y = (size - frame.height) // 2

        frame_canvas.alpha_composite(
            frame,
            (x, y)
        )

        frames.append(
            ImageTk.PhotoImage(frame_canvas)
        )

    return frames


# =========================================================
# LOAD OUTER GIFS
# =========================================================

frames1 = load_gif(
    GIF1,
    GIF_SIZE
)

frames2 = load_gif(
    GIF2,
    GIF_SIZE
)

frames3 = load_gif(
    GIF3,
    GIF3_SIZE
)


# =========================================================
# LOAD CENTER GIFS
#
# وسط:
# حالت عادی  = GIF2
# Hover       = GIF1
# Click       = GIF3
# =========================================================

center_frames_normal = load_gif(
    GIF2,
    CENTER_GIF_SIZE
)

center_frames_hover = load_gif(
    GIF1,
    CENTER_GIF_SIZE
)

center_frames_click = load_gif(
    GIF3,
    CENTER_GIF_SIZE
)


# =========================================================
# MAIN CANVAS
# =========================================================

canvas = tk.Canvas(
    root,
    width=WINDOW_SIZE,
    height=WINDOW_SIZE,
    bg=TRANSPARENT_COLOR,
    highlightthickness=0,
    bd=0
)

canvas.pack()

center = WINDOW_SIZE // 2


# =========================================================
# MAIN CIRCLE
# =========================================================

canvas.create_oval(
    12,
    12,
    WINDOW_SIZE - 12,
    WINDOW_SIZE - 12,
    fill="#050505",
    outline="#303030",
    width=3
)


# =========================================================
# INNER RING
# =========================================================

canvas.create_oval(
    25,
    25,
    WINDOW_SIZE - 25,
    WINDOW_SIZE - 25,
    outline="#151515",
    width=2
)


# =========================================================
# CENTER RING
# =========================================================

canvas.create_oval(
    center - 92,
    center - 92,
    center + 92,
    center + 92,
    outline="#181818",
    width=2
)


# =========================================================
# CLOCK MARKERS
# =========================================================

marker_radius = 270

for i in range(12):

    angle = math.radians(
        i * 30 - 90
    )

    x = (
        center
        +
        math.cos(angle) * marker_radius
    )

    y = (
        center
        +
        math.sin(angle) * marker_radius
    )

    canvas.create_oval(
        x - 2,
        y - 2,
        x + 2,
        y + 2,
        fill="#353535",
        outline=""
    )


# =========================================================
# CENTER GIF VARIABLES
# =========================================================

# مهم:
# در شروع GIF2 نمایش داده می شود

center_current_frames = center_frames_normal

center_frame_index = 0

center_mouse_inside = False

center_click_mode = False

center_pressed = False
center_dragging = False

center_press_x = 0
center_press_y = 0


# =========================================================
# CENTER IMAGE
# =========================================================

center_image_id = canvas.create_image(
    center,
    center,
    image=center_frames_normal[0]
)


# =========================================================
# CENTER TEXT
# =========================================================

system_text_id = canvas.create_text(
    center,
    center - 12,
    text="SYSTEM",
    fill="#777777",
    font=("Arial", 16, "bold")
)


dariush_text_id = canvas.create_text(
    center,
    center + 16,
    text="DARIUSH DERKI",
    fill="#D4AF37",
    font=("Arial", 12, "bold")
)


# =========================================================
# PLAY CENTER GIF
# =========================================================

def play_center_gif():

    global center_frame_index

    if not root.winfo_exists():
        return

    if not center_current_frames:
        return

    center_frame_index += 1

    if (
        center_frame_index
        >= len(center_current_frames)
    ):
        center_frame_index = 0

    canvas.itemconfig(
        center_image_id,
        image=center_current_frames[
            center_frame_index
        ]
    )

    # متن همیشه روی GIF باشد
    canvas.tag_raise(
        system_text_id
    )

    canvas.tag_raise(
        dariush_text_id
    )

    root.after(
        70,
        play_center_gif
    )


# =========================================================
# SET CENTER GIF
# =========================================================

def set_center_gif(frames):

    global center_current_frames
    global center_frame_index

    center_current_frames = frames

    center_frame_index = 0

    if frames:

        canvas.itemconfig(
            center_image_id,
            image=frames[0]
        )

    # متن دوباره روی GIF
    canvas.tag_raise(
        system_text_id
    )

    canvas.tag_raise(
        dariush_text_id
    )


# =========================================================
# CENTER MOUSE POSITION
# =========================================================

def center_is_inside(event):

    dx = event.x - center
    dy = event.y - center

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    return distance <= (
        CENTER_GIF_SIZE / 2
    )


# =========================================================
# CENTER HOVER
# =========================================================

def center_motion(event):

    global center_mouse_inside

    inside = center_is_inside(event)

    # -----------------------------------------------------
    # ورود ماوس به مرکز
    # GIF2 ---> GIF1
    # -----------------------------------------------------

    if inside and not center_mouse_inside:

        center_mouse_inside = True

        canvas.configure(
            cursor="hand2"
        )

        if not center_click_mode:

            set_center_gif(
                center_frames_hover
            )

    # -----------------------------------------------------
    # خروج ماوس از مرکز
    # GIF1 ---> GIF2
    # -----------------------------------------------------

    elif (
        not inside
        and
        center_mouse_inside
    ):

        center_mouse_inside = False

        canvas.configure(
            cursor=""
        )

        if not center_click_mode:

            set_center_gif(
                center_frames_normal
            )


# =========================================================
# CENTER PRESS
# =========================================================

def center_press(event):

    global center_pressed
    global center_dragging
    global center_press_x
    global center_press_y

    if not center_is_inside(event):

        return

    center_pressed = True

    center_dragging = False

    center_press_x = event.x_root
    center_press_y = event.y_root

    start_window_drag(event)

    return "break"


# =========================================================
# CENTER DRAG
# =========================================================

def center_button_motion(event):

    global center_dragging

    if not center_pressed:

        return "break"

    dx = (
        event.x_root
        -
        center_press_x
    )

    dy = (
        event.y_root
        -
        center_press_y
    )

    if (
        abs(dx) > DRAG_THRESHOLD
        or
        abs(dy) > DRAG_THRESHOLD
    ):

        center_dragging = True

    if center_dragging:

        move_window(event)

    return "break"


# =========================================================
# CENTER RELEASE
# =========================================================

def center_release(event):

    global center_pressed
    global center_dragging

    if not center_pressed:

        return "break"

    center_pressed = False

    # اگر حرکت نکرده باشد = کلیک
    if not center_dragging:

        if center_is_inside(event):

            center_clicked()

    stop_window_drag(event)

    center_dragging = False

    return "break"


# =========================================================
# CENTER CLICK
# =========================================================

def center_clicked():

    global center_click_mode

    if center_click_mode:

        return

    center_click_mode = True

    # -----------------------------------------------------
    # BEEP
    # -----------------------------------------------------

    try:

        winsound.Beep(
            880,
            100
        )

    except:

        try:
            winsound.MessageBeep()

        except:
            pass

    # -----------------------------------------------------
    # GIF3
    # -----------------------------------------------------

    set_center_gif(
        center_frames_click
    )

    # -----------------------------------------------------
    # PRESS EFFECT
    # -----------------------------------------------------

    canvas.scale(
        center_image_id,
        center,
        center,
        0.93,
        0.93
    )

    root.after(
        100,
        center_release_effect
    )

    # -----------------------------------------------------
    # FINISH CLICK
    # -----------------------------------------------------

    root.after(
        CLICK_GIF_TIME,
        finish_center_click
    )


# =========================================================
# CENTER RELEASE EFFECT
# =========================================================

def center_release_effect():

    canvas.scale(
        center_image_id,
        center,
        center,
        1.075,
        1.075
    )


# =========================================================
# FINISH CENTER CLICK
# =========================================================

def finish_center_click():

    global center_click_mode
    global center_mouse_inside

    center_click_mode = False

    # وضعیت واقعی ماوس را دوباره بررسی می کنیم

    if center_is_inside_current_mouse():

        center_mouse_inside = True

        set_center_gif(
            center_frames_hover
        )

    else:

        center_mouse_inside = False

        set_center_gif(
            center_frames_normal
        )


# =========================================================
# CURRENT MOUSE POSITION
# =========================================================

def center_is_inside_current_mouse():

    try:

        x = root.winfo_pointerx()
        y = root.winfo_pointery()

        wx = root.winfo_rootx()
        wy = root.winfo_rooty()

        local_x = x - wx
        local_y = y - wy

        dx = local_x - center
        dy = local_y - center

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        return distance <= (
            CENTER_GIF_SIZE / 2
        )

    except:

        return False


# =========================================================
# CENTER EVENTS
# =========================================================

canvas.bind(
    "<Motion>",
    center_motion,
    add="+"
)

canvas.bind(
    "<ButtonPress-1>",
    center_press,
    add="+"
)

canvas.bind(
    "<B1-Motion>",
    center_button_motion,
    add="+"
)

canvas.bind(
    "<ButtonRelease-1>",
    center_release,
    add="+"
)


# =========================================================
# OUTER GIF BUTTON CLASS
# =========================================================

class GifButton:

    def __init__(
        self,
        parent,
        frames1,
        frames2,
        frames3,
        x,
        y
    ):

        self.parent = parent

        self.frames1 = frames1
        self.frames2 = frames2
        self.frames3 = frames3

        self.current_frames = self.frames1

        self.index = 0

        self.mouse_inside = False

        self.click_mode = False

        self.button_pressed = False
        self.button_dragging = False

        self.press_x = 0
        self.press_y = 0

        # -------------------------------------------------
        # Canvas
        # -------------------------------------------------

        self.canvas = tk.Canvas(
            parent,
            width=GIF_SIZE,
            height=GIF_SIZE,
            bg="#050505",
            highlightthickness=0,
            bd=0
        )

        self.canvas.place(
            x=x,
            y=y
        )

        # -------------------------------------------------
        # GIF
        # -------------------------------------------------

        self.image_id = self.canvas.create_image(
            GIF_SIZE // 2,
            GIF_SIZE // 2,
            image=self.frames1[0]
        )

        # -------------------------------------------------
        # Events
        # -------------------------------------------------

        self.canvas.bind(
            "<Enter>",
            self.mouse_enter
        )

        self.canvas.bind(
            "<Leave>",
            self.mouse_leave
        )

        self.canvas.bind(
            "<ButtonPress-1>",
            self.button_press
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.button_motion
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.button_release
        )

        self.canvas.bind(
            "<ButtonPress-2>",
            self.middle_press
        )

        self.canvas.bind(
            "<B2-Motion>",
            self.middle_motion
        )

        self.canvas.bind(
            "<ButtonRelease-2>",
            self.middle_release
        )

        self.play()


    # =====================================================
    # PLAY
    # =====================================================

    def play(self):

        if not self.canvas.winfo_exists():
            return

        if not self.current_frames:
            return

        self.index += 1

        if (
            self.index
            >= len(self.current_frames)
        ):

            self.index = 0

        self.canvas.itemconfig(
            self.image_id,
            image=self.current_frames[
                self.index
            ]
        )

        self.canvas.after(
            70,
            self.play
        )


    # =====================================================
    # SET GIF
    # =====================================================

    def set_gif(self, frames):

        self.current_frames = frames

        self.index = 0

        if frames:

            self.canvas.itemconfig(
                self.image_id,
                image=frames[0]
            )


    # =====================================================
    # MOUSE ENTER
    # =====================================================

    def mouse_enter(self, event):

        self.mouse_inside = True

        self.canvas.configure(
            cursor="hand2"
        )

        if not self.click_mode:

            self.set_gif(
                self.frames2
            )


    # =====================================================
    # MOUSE LEAVE
    # =====================================================

    def mouse_leave(self, event):

        self.mouse_inside = False

        self.canvas.configure(
            cursor=""
        )

        if not self.click_mode:

            self.set_gif(
                self.frames1
            )


    # =====================================================
    # BUTTON PRESS
    # =====================================================

    def button_press(self, event):

        self.button_pressed = True

        self.button_dragging = False

        self.press_x = event.x_root
        self.press_y = event.y_root

        start_window_drag(event)


    # =====================================================
    # BUTTON MOTION
    # =====================================================

    def button_motion(self, event):

        if not self.button_pressed:

            return

        dx = (
            event.x_root
            -
            self.press_x
        )

        dy = (
            event.y_root
            -
            self.press_y
        )

        if (
            abs(dx) > DRAG_THRESHOLD
            or
            abs(dy) > DRAG_THRESHOLD
        ):

            self.button_dragging = True

        if self.button_dragging:

            move_window(event)


    # =====================================================
    # BUTTON RELEASE
    # =====================================================

    def button_release(self, event):

        if not self.button_pressed:

            return

        self.button_pressed = False

        if not self.button_dragging:

            self.clicked(event)

        stop_window_drag(event)

        self.button_dragging = False


    # =====================================================
    # CLICK
    # =====================================================

    def clicked(self, event):

        if self.click_mode:

            return

        self.click_mode = True

        # -------------------------------------------------
        # BEEP
        # -------------------------------------------------

        try:

            winsound.Beep(
                880,
                100
            )

        except:

            try:
                winsound.MessageBeep()

            except:
                pass

        # -------------------------------------------------
        # GIF3
        # -------------------------------------------------

        self.set_gif(
            self.frames3
        )

        self.press_effect()

        self.canvas.after(
            CLICK_GIF_TIME,
            self.finish_click
        )


    # =====================================================
    # PRESS EFFECT
    # =====================================================

    def press_effect(self):

        self.canvas.scale(
            self.image_id,
            GIF_SIZE // 2,
            GIF_SIZE // 2,
            0.90,
            0.90
        )

        self.canvas.after(
            100,
            self.release_effect
        )


    # =====================================================
    # RELEASE EFFECT
    # =====================================================

    def release_effect(self):

        self.canvas.scale(
            self.image_id,
            GIF_SIZE // 2,
            GIF_SIZE // 2,
            1.111,
            1.111
        )


    # =====================================================
    # FINISH CLICK
    # =====================================================

    def finish_click(self):

        self.click_mode = False

        if self.mouse_inside:

            self.set_gif(
                self.frames2
            )

        else:

            self.set_gif(
                self.frames1
            )


    # =====================================================
    # MIDDLE MOUSE
    # =====================================================

    def middle_press(self, event):

        start_window_drag(event)


    def middle_motion(self, event):

        move_window(event)


    def middle_release(self, event):

        stop_window_drag(event)


# =========================================================
# CREATE 12 OUTER BUTTONS
# =========================================================

buttons = []

for i in range(12):

    angle = math.radians(
        i * 30 - 90
    )

    button_center_x = (
        center
        +
        math.cos(angle)
        *
        BUTTON_RADIUS
    )

    button_center_y = (
        center
        +
        math.sin(angle)
        *
        BUTTON_RADIUS
    )

    button_x = (
        button_center_x
        -
        GIF_SIZE / 2
    )

    button_y = (
        button_center_y
        -
        GIF_SIZE / 2
    )

    button = GifButton(
        root,
        frames1,
        frames2,
        frames3,
        button_x,
        button_y
    )

    buttons.append(button)


# =========================================================
# CLOSE BUTTON
# =========================================================

close_btn = tk.Button(
    root,
    text="×",
    command=root.destroy,
    font=("Arial", 17, "bold"),
    bg="#050505",
    fg="#555555",
    activebackground="#111111",
    activeforeground="#ffffff",
    bd=0,
    highlightthickness=0,
    cursor="hand2"
)

close_btn.place(
    x=535,
    y=38,
    width=35,
    height=35
)


# =========================================================
# START CENTER ANIMATION
# =========================================================

play_center_gif()


# =========================================================
# RUN
# =========================================================

root.mainloop()
