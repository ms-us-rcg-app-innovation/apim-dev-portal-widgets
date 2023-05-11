import { RequestBase } from "./requestBase"

export class DeleteProductRequest extends RequestBase {
    public productId: string;

    constructor(sasToken: string, productId: string) {
        super(sasToken);
        this.productId = productId;
    }
}