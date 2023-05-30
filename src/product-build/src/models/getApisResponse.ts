import { ResponseBase } from "./responseBase";
import { Api } from "./api";

export class GetApisResponse extends ResponseBase {
    public apis?: Api[]
}