{
  header: {
    university: {
        type: String,
        required: true
    },
    college: {
        type: String,
        required: true
    },
    route: {
        type: String,
        required: true
    },
  },
  sections: [
    {
      section_name: { type: String. required: true },
      info: { type: String, required: true },
      articulations: [
        {
          univ: {
            // can be an object with keys "or", "and"
            // can be of type String with reference to course ObjectId
            type: mongoose.Schema.Mixed 
          },
          cc: {
            // can be an object with keys "or", "and"
            // can be of type String with reference to course ObjectId
            type: mongoose.Schema.Mixed
          },
          or: [{
            univ: {
              // can be an object with keys "or", "and"
              // can be of type String with reference to course ObjectId
              type: mongoose.Schema.Mixed
            },
            cc: {
              // can be an object with keys "or", "and"
              // can be of type String with reference to course ObjectId
              type: mongoose.Schema.Mixed
            }
          }]
        }
      ],
    },
  ],
}