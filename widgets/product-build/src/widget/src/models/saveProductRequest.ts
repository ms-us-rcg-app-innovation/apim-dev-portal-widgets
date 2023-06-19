import { RequestBase } from "./requestBase"
import { Product } from "./product"

export class SaveProductRequest extends RequestBase {
    public product: Product;

    constructor(sasToken: string, product: Product) {
        super(sasToken);
        this.product = product;
    }

    get path() {
        return `/create_product`;
    } 

    get body() {
        return JSON.stringify(this.product);
    }
}