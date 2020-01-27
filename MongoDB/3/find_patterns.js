find_patterns = function () {

	numeros = db.phones.find().toArray();

	var capicua_count = 0;
	var capicuas = []


	for(var i = 0; i < numeros.length; i++){
		var temp = numeros[i]['_id']
		temp = (temp - numeros[i]['components']['country'] * 1000000000).toString();
		if( temp == temp.split("").reverse().join("") ){
			// is a capicua
			capicua_count = capicua_count + 1;
			capicuas.push(temp);
		}
	}

	print(capicua_count);
	print(capicuas);
	
}
