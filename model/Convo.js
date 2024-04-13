import { UUID } from 'mongodb';
import mongoose from 'mongoose';
const { Schema, model } = mongoose;

const convoSchema = new Schema({
  name: String,
  userId: UUID,
  msgHistory: [String]
});

const Convo = model('Convo', convoSchema);
export default Convo;