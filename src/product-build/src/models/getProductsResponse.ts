import { ResponseBase } from "./responseBase";
import { Product } from "./product";

export class GetProductsResponse extends ResponseBase {
    public products?: Product[]
}