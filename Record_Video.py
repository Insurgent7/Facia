def live():
    import cv2
    import datetime
# records video from the same cameras. (Can replace CCTV).

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to read camera feed")
    cap.set(3, 1280)
    cap.set(4, 1024)
    frameyowidth = int(cap.get(3))
    frameyoheight = int(cap.get(4))
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frameyowidth, frameyoheight))
    while True:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow("Live Feed", frame)
            # Press Esc on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == 27:
                break
        # Break the loop
        else:
            break
    cap.release()
    out.release()
    # Closes all the frames
    cv2.destroyAllWindows()
live()