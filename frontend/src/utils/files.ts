export function convertKbToReadableSize(kb: number): string {
    if (kb < 0) {
        throw new Error("KB size cannot be negative.");
    }

    const mb = kb / 1024;
    const gb = mb / 1024;

    if (gb >= 1) {
        return `${gb.toFixed(2)} GB`;
    } else if (mb >= 1) {
        return `${mb.toFixed(2)} MB`;
    } else {
        return `${kb} KB`;
    }
}