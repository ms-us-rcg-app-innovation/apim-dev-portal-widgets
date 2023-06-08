export class Utils {
    public static getResourceName(resource: string, fullId: string, resultType: string = "name"): string {
        const regexp = new RegExp(`\/${resource}\/(?!${resource})(.*)`); // negative lookahead to escape cases when "resource" is in "fullId" multiple times in a row (e.g. ...apis/operations/operations/foo - https://github.com/Azure/api-management-developer-portal/issues/2112 )
        const matches = regexp.exec(fullId);

        if (matches && matches.length > 1) {
            switch (resultType) {
                case "name":
                    return matches[1];

                case "shortId":
                    return `/${resource}/${matches[1]}`;

                default:
                    throw new Error(`Unknown resultType: ${resultType}`);
            }
        } else {
            throw new Error("Could not parse ID.");
        }
    }
}
