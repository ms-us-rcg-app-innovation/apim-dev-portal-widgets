export class RequestBase {
    public sasToken: string;

    constructor(sasToken: string) {
        this.sasToken = sasToken;
    }
}