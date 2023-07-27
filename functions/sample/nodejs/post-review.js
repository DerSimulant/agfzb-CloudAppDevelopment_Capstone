const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    // Authenticating with the service
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator });
    cloudant.setServiceUrl(params.COUCH_URL);

    try {
        // Create a new document (review) with the provided details
        const response = await cloudant.postDocument({
            db: 'reviews',
            document: params.review // The review details should be passed in under the 'review' key
        });

        // Return the result of the operation
        if (response.result.ok) {
            return { result: 'Review successfully added' };
        } else {
            return { error: 'Error in adding the review' };
        }
    } catch (error) {
        console.error('Error:', error);
        if (error.statusCode === 404) {
            return { error: 'The database is empty' };
        } else {
            return { error: 'Something went wrong on the server' };
        }
    }
}
