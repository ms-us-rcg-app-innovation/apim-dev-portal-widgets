import { RequestBase } from "./requestBase"

export class DeleteProductRequest extends RequestBase {
    public productId: string;

    constructor(sasToken: string, productId: string) {
        super(sasToken);
        this.productId = productId;
    }

    get path() {
        return `/delete_product?productId=${this.productId}`;
    } 
}