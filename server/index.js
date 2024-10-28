const express = require('express');
const cors = require('cors');

const { MongoClient } = require('mongodb');
const dotenv = require('dotenv');

dotenv.config();
const app = express();
app.use(cors());

const port = 80;

const uri = process.env.MONGODB_URI;

const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

client.connect()
    .then(() => {
        console.log('Connected to MongoDB Atlas');

        const database = client.db('tech-news-db');
        const tcCollection = database.collection('techcrunch');
        const teuCollection = database.collection('techeu');
        const thevergeCollection = database.collection('theverge');

        app.get('/techcrunch', async (req, res) => {
            try {
                const limit = parseInt(req.query.limit) || 10;
                const documents = await tcCollection.find().limit(limit).sort({ published_datetime: -1 }).toArray();
                res.json(documents);
            } catch (error) {
                res.status(500).send('Error fetching documents: ' + error.message);
            }
        });

        app.get('/techeu', async (req, res) => {
            try {
                const limit = parseInt(req.query.limit) || 10;
                const documents = await teuCollection.find().limit(limit).toArray();
                res.json(documents);
            } catch (error) {
                res.status(500).send('Error fetching documents: ' + error.message);
            }
        });

        app.get('/theverge', async (req, res) => {
            try {
                const limit = parseInt(req.query.limit) || 10;
                const documents = await thevergeCollection.find().limit(limit).toArray();
                res.json(documents);
            } catch (error) {
                res.status(500).send('Error fetching documents: ' + error.message);
            }
        });

        // Step 4: Start the server
        app.listen(port, () => {
            console.log(`Server is running on http://localhost:${port}`);
        });
    })
    .catch(error => {
        console.error('Error connecting to MongoDB Atlas: ', error);
    });