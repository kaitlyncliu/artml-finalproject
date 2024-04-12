import mongoose from 'mongoose';
import Convo from './model/Convo.js';
import dotenv from 'dotenv';

dotenv.config({ silent: true }); // Suppress warnings if no .env file is found

mongoose.connect(process.env.MONGO_URI)


const conversation = new Convo({
    user: "Kaitlyn Liu",
    msgHistory: ["Hi there, I'm Kaitlyn"],
  });

await conversation.save();

// Find a single blog post
const firstConvo = await Convo.findOne({});
console.log(firstConvo);