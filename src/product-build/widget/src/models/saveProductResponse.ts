import { ResponseBase } from "./responseBase";
import { Product } from "./product";

export class SaveProductResponse extends ResponseBase {
    public product?: Product
}