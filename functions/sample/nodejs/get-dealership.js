const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(params.COUCH_URL);

    try {
        let dealerships = [];

        if (params.state) {
            // Filter by state if state parameter is provided
            const result = await cloudant.postFind({
                db: 'dealerships',
                selector: { 'st': params.state }
            });
            dealerships = result.result.docs;
        } else {
            // Retrieve all documents if state parameter is not provided
            const result = await cloudant.postAllDocs({
                db: 'dealerships',
                includeDocs: true
            });
            dealerships = result.result.rows.map(row => row.doc);
        }

        // Return the results
        return { "dealerships": dealerships };
    } catch (error) {
        console.error('Error:', error);
        if (error.statusCode === 404) {
            return { error: 'The database is empty' };
        } else {
            return { error: 'Something went wrong on the server' };
        }
    }
}
