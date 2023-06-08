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
     * Description of API.
     */
    public description?: string;

    /**
     * API URL suffix, e.g. "/httbin"
     */
    public path?: string;

}