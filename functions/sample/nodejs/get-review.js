const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(params.COUCH_URL);

    try {
        let reviews = [];

        if (params.dealership) {
            // Filter by dealership if dealership_id parameter is provided
            const result = await cloudant.postFind({
                db: 'reviews',
                selector: { 'dealership': params.dealership }
            });
            reviews = result.result.docs;
        } else {
            // Retrieve all documents if dealership_id parameter is not provided
            const result = await cloudant.postAllDocs({
                db: 'reviews',
                includeDocs: true
            });
            reviews = result.result.rows.map(row => row.doc);
        }

        // Return the results
        return { "reviews": reviews };
    } catch (error) {
        console.error('Error:', error);
        if (error.statusCode === 404) {
            return { error: 'The database is empty' };
        } else {
            return { error: 'Something went wrong on the server' };
        }
    }
}
