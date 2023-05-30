import { RequestBase } from "./requestBase"

export class GetApisRequest extends RequestBase {
    public productId: string;

    constructor(sasToken: string, productId: string) {
        super(sasToken);
        this.productId = productId;
    }

    get path() {
        return `/list_apis_of_products?productIds=${this.productId}`;
    } 
}