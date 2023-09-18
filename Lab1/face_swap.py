import cv2
import numpy as np
import time
import face_detect

def combine_with_mask(image1, image2, mask):
    """Returns an image that is image2 where mask == true, otherwise image1"""

    inverse_mask = cv2.bitwise_not(mask)
    result = cv2.bitwise_and(image1, image1, mask=inverse_mask)
    image2_part = cv2.bitwise_and(image2, image2, mask=mask)
    final_result = cv2.add(result, image2_part)

    return final_result

def swap_faces(original_image, output_image, face_orderings, oval, order_offset):
    """Modifies output_image to swap faces according to face_orderings"""

    # when mapping_order_offset == len(face_mappings), then no swaps happen
    if order_offset == len(face_orderings):
        order_offset += 1

    for face_ordering_idx, face_ordering in enumerate(face_orderings):
        face = face_ordering.face
        try:
            next_face_ordering_idx = (face_ordering_idx + order_offset) % len(face_orderings)
            next_face_ordering_data = face_orderings[next_face_ordering_idx]
            next_face = next_face_ordering_data.face

            face_crop = original_image[face.y:face.y2, face.x:face.x2]
            face_resized = cv2.resize(face_crop, (next_face.w, next_face.h))

            if oval:
                oval_mask = np.zeros(face_resized.shape[:2], dtype=np.uint8)
                size = (int(next_face.w / 2), int(next_face.h / 2))
                cv2.ellipse(oval_mask, size, size, 0, 0, 360, 255, -1)

                face_resized_masked = cv2.bitwise_and(face_resized, face_resized, mask=oval_mask)
                
                next_face_crop = output_image[next_face.y:next_face.y2, next_face.x:next_face.x2]
                face_to_paste = combine_with_mask(next_face_crop, face_resized_masked, oval_mask)
                next_face_crop[:] = face_to_paste
            else:
                output_image[next_face.y:next_face.y2, next_face.x:next_face.x2] = face_resized
        except:
            pass

def blur_edges(output_image, face_orderings, blur_thickness, blur_radius, oval):
    """Returns an image with blurred connections between the pasted faces and the background"""
    if len(face_orderings) == 0:
        return output_image
    
    if blur_radius % 2 == 0:
        blur_radius += 1
    blurred_image = cv2.medianBlur(output_image, blur_radius)

    mask = np.zeros(output_image.shape[:2], dtype=np.uint8)

    for face_ordering_data in face_orderings:
        face = face_ordering_data.face
        if oval:
            size = (int(face.w / 2), int(face.h / 2))
            cv2.ellipse(mask, face.get_center_tuple_int(), size, 0, 0, 360, 255, blur_thickness)
        else:
            cv2.rectangle(
                mask,
                (face.x, face.y),
                (face.x2, face.y2),
                255,
                blur_thickness,
            )

    final_result = combine_with_mask(output_image, blurred_image, mask)

    return final_result


def video_detection(original_video, args):
    """Sets up and then continuously runs the face swap on the video"""

    if not original_video.isOpened():
        raise Exception("Could not open video")
    
    if args["save"] is not None:
        fps = original_video.get(cv2.CAP_PROP_FPS)
        delta = 1 / fps
        width = int(original_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(original_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        extension_to_fourcc = {
            "avi": "XVID",
            "mp4": "mp4v",
            "mov": "mp4v",
            "mkv": "XVID",
        }
        extension = args["save"].split(".")[-1]
        fourcc = extension_to_fourcc.get(extension, None)

        if fourcc is None:
            raise Exception("Invalid save extension. Must be avi, mp4, mov, or mkv.")

        video_writer_fourcc = cv2.VideoWriter_fourcc(*fourcc)
        output_video = cv2.VideoWriter(args["save"], video_writer_fourcc, fps, (width, height))
    else:
        t0 = time.time()
        t1 = time.time()
        delta = 1 / 30

    face_orderings = []

    while original_video.isOpened():
        ret, frame = original_video.read()

        if not ret:
            break

        output_frame = frame.copy()
        
        face_detect.detect_faces_and_update_ordering(frame, args["confidence"], face_orderings, args["wait_time"], delta)
        swap_faces(frame, output_frame, face_orderings, args["oval"], args["order_offset"])

        if args["blur"]:
            output_frame = blur_edges(output_frame, face_orderings, args["blur_thickness"], args["blur_radius"], args["oval"])

        if args["debug"]:
            for face_ordering_data in face_orderings:
                face_ordering_data.draw_debug(output_frame, args["wait_time"])

            # fps text (bottom left)
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (5, output_frame.shape[0] - 5)
            fontScale = 0.5
            fontColor = (0, 0, 255)
            thickness = 1
            lineType = 2
            text = "Output FPS: %.2f" % (1 / delta)
            cv2.putText(
                output_frame,
                text,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType,
            )

        if args["save"] is not None:
            output_video.write(output_frame)
        else:
            t1 = time.time()
            delta = t1 - t0
            t0 = t1

        cv2.imshow("Face Swap Pro Plus Platinum Edition Deluxe", output_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    original_video.release()

    if args["save"] is not None:
        output_video.release()

    cv2.destroyAllWindows()

def image_detection(original_image, args):
    """Sets up and then runs the face swap on the image"""

    while True:
        output_image = original_image.copy()
        faces = face_detect.detect_faces(original_image, args["confidence"])

        if len(faces) < 2:
            raise Exception(f"Need at least two faces to swap (only detected {len(faces)})")
        
        face_orderings = [face_detect.FaceOrderingData(face) for face in faces]
        swap_faces(original_image, output_image, face_orderings, args["oval"], args["order_offset"])

        if args["blur"]:
            output_image = blur_edges(output_image, face_orderings, args["blur_thickness"], args["blur_radius"], args["oval"])

        if args["debug"]:
            for face in faces:
                face.draw_debug(output_image)

        if args["save"] is not None:
            cv2.imwrite(args["save"], output_image)

        cv2.imshow("Face Swap Pro Plus Platinum Edition Deluxe", output_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break