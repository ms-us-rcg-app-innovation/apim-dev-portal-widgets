import { VersionSet } from "./versionSet";
import { ApiContract, ContactDetails, LicenseDetails, SubscriptionKeyParameterName } from "./apiContract";
import { Utils } from "../utils";
import { AuthenticationSettings } from "./authenticationSettings";
import { TypeOfApi } from "./types";

/**
 * API model.
 */
export class Api {
    /**
     * Unique ARM identifier.
     */
    public id: string;

    /**
     * Unique API identifier.
     */
    public name: string;

    /**
     * Display name of API, e.g. "HTTP Bin".
     */
    public displayName?: string;

    /**
     * Display name of API that includes version.
     */
    public versionedDisplayName?: string;

    /**
     * Description of API.
     */
    public description?: string;


    /**
     * Web service URL "https://httpbin.org".
     */
    public serviceUrl?: string;

    /**
     * API URL suffix, e.g. "/httbin"
     */
    public path?: string;

    /**
     * Determines type of API, e.g. "soap".
     */
    public type?: string;
    
    /**
     * Determines type name of API to display in UI, e.g. "Soap".
     */
    public typeName?: string;

}