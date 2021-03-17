const chai = require('chai');
const assert = chai.assert;
const chaiHTTP = require('chai-http');
const expect = chai.expect;
const KGMLFilePath1 = './temp_uploads/ko00010.xml';
//const KGMLFilePath2 = './temp_uploads/ko02040.xml';
//const api = require('../server/routes/api').router;

chai.use(chaiHTTP);

describe('App', function(){

  it('App should return the files of the server', function(){
    chai.request('http://localhost:3000')
      .get('/api/files')
      .end(function (err, res) {
        expect(err).to.be.null;
        expect(res).to.be.not.null;
      });
  });

  it('App should upload an xml file to the server', function(){
    chai.request('http://localhost:3000/api')
      .post('/upload')
      .set('content-type', 'application/xml')
      .attach('file', KGMLFilePath1 , 'ko04066.xml')
      .end(function(err, res){
        expect(err).to.be.null;
        expect(res).to.be.not.null;
      });
  });

  it('App should delete last file uploaded to the server', function(){
    chai.request('http://localhost:3000/api')
      .delete('/delete')

  });

});

