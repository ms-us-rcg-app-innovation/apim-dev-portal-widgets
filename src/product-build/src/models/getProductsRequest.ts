import { RequestBase } from "./requestBase"

export class GetProductsRequest extends RequestBase {
    public baseProductTag?: string;

    constructor(sasToken: string, baseProductTag?: string) {
        super(sasToken);
        this.baseProductTag = baseProductTag;
    }

    get path() {
        if (this.baseProductTag) {
            return `/list_tagged_products?tagIds=${this.baseProductTag}`
        } else {
            return `/list_user_products`
        }
    } 
}