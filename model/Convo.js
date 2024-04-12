import mongoose from 'mongoose';
const { Schema, model } = mongoose;

const convoSchema = new Schema({
  user: String,
  msgHistory: [String]
});

const Convo = model('Convo', convoSchema);
export default Convo;