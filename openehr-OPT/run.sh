# copy templates folder (containing opt files) here

docker build -t openehr-opt .

docker run -it -v ./composition_outs:/composition_outs -e PATH=/usr/share/groovy/bin:$PATH -e GROOVY_HOME=/usr/share/groovy/ openehr-opt bash 

# gradle build -x test

mkdir /composition_outs/version
./opt.sh ingen templates/patient.opt /composition_outs/version 1 json version
./opt.sh ingen templates/diagnosis_demo.opt /composition_outs/version 1 json version
./opt.sh ingen templates/vital_signs.opt /composition_outs/version 1 json version

mkdir /composition_outs/locatable
./opt.sh ingen templates/patient.opt /composition_outs/locatable 1 json locatable
./opt.sh ingen templates/diagnosis_demo.opt /composition_outs/locatable 1 json locatable
./opt.sh ingen templates/vital_signs.opt /composition_outs/locatable 1 json locatable

## DOC:
# ./opt.sh ingen path_to_opt dest_folder [amount] [json|xml] [version|composition] [withParticipations]
# 
#    amount: defines how many XML instances will be generated, default is 1
#   format: 'json' or 'xml', default is 'json'
#    object: type of openEHR object to generate, 'version' or 'composition', default is 'version'
#    withParticipations: if included in the parameters, it will add participations to the composition
