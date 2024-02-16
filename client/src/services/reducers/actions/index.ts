import { IMAGE_FILES } from "./types";

export function uploadImages(images: any) {
    return {
        type: IMAGE_FILES,
        payload: images
    }
}