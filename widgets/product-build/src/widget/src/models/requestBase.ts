export class RequestBase {
    public sasToken: string;

    constructor(sasToken: string) {
        this.sasToken = sasToken;
    }

    get headers() : HeadersInit {
        return {
            "Content-Type": "application/json",
            "Authorization": this.sasToken
        }
    }
}