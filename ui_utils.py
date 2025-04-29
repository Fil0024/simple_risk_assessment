import matplotlib.pyplot as plt

def maximize_window(fig):
    mngr = fig.canvas.manager
    try:
        mngr.window.showMaximized()
    except AttributeError:
        try:
            mngr.window.state('zoomed')
        except Exception:
            mngr.full_screen_toggle()