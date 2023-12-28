import cv2 as cv

def main():
    # access webcam
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
   
    while True:
        # pull frame
        ret, frame = cap.read()
        # mirror frame
        frame = cv.flip(frame, 1)
        # display frame
        cv.imshow('frame',frame)
        if cv.waitKey(1) == ord('q'):
            break

    # release everything
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
   main()