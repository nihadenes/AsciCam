## AsciCam.

AsciCam is a program that converts your camera input into ascii while the pogram is open.


## Getting Started.

### Install Requirements

```
pip install -r requirements.txt
```

Now that's it! You should be able to run the code.

![Screenshot_1](https://user-images.githubusercontent.com/91975592/179146361-3cb72e3b-310b-41e4-a452-8483eb5eb30e.png)


![Screenshot_3](https://user-images.githubusercontent.com/91975592/179146595-7679749c-0ac8-41b3-b051-3bd611d51082.png)

(Shot by Logitech C525)

## Configurating the code.

There are configuration variables that you can change between 129. and 135. lines.

### Meanings of the configuration variables.

```

    camera: Which camera to use? (As a number)
    mirrored: Mirror the camera. (1 or 0)
    vertical: Character number in a row.
    fontsize: Fontsize of the terminal for smooth views. (Doesn't work in linux, don't use "3" because it's buggy right now.)

    set_screen: Fitting the terminal into ascii characters. (0 is for true and 1 is for false.)
    char_list: Characters listed by their brightness.

```
