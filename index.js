import mongoose from 'mongoose';
import { ObjectId } from 'mongodb';
import Convo from './model/Convo.js';
import dotenv from 'dotenv';

dotenv.config({ silent: true }); // Suppress warnings if no .env file is found

mongoose.connect(process.env.MONGO_URI)


async function createConvo(userName, msgHistory) {
    const convo = await Convo.create({
        name: userName,
        msgHistory: msgHistory
      });
    return convo
}

async function addMsg(userId, newMsgs) {
    console.log(userId)
    const convo = await Convo.findById(userId)
    console.log(convo)
    convo.msgHistory = [...convo.msgHistory, ...newMsgs]
    await convo.save();
    return convo
}

async function deleteUserAndHistory(userId) {
    const convo = await Convo.findById(userId);
    const del = Convo.deleteOne({"_id": new ObjectId(userId)})
}

const convo = await createConvo("Kaitlyn Liu 2", ["HIIII"]);
console.log(convo)
await addMsg(convo._id, ["helllooo"]);
console.log(convo)

deleteUserAndHistory(convo.ObjectId)