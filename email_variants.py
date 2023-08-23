def gen_email_variants(firstname, lastname, domain):	
	email_variants = [

    # REGULAR

        f"{firstname}.{lastname}@{domain}", #firstname.lastname@test.com
        f"{firstname[0]}.{lastname}@{domain}", #f.lastname@test.com
        f"{firstname}.{lastname[0]}@{domain}", #firstname.l@test.com

        f"{firstname}-{lastname}@{domain}", #firstname-lastname@test.com
        f"{firstname[0]}-{lastname}@{domain}", #f-lastname@test.com
        f"{firstname}-{lastname[0]}@{domain}", #firstname-l@test.com

        f"{firstname}_{lastname}@{domain}", #firstname_lastname@test.com
        f"{firstname[0]}_{lastname}@{domain}", #f_lastname@test.com
        f"{firstname}_{lastname[0]}@{domain}", #firstname_l@test.com

        f"{firstname}{lastname}@{domain}", #firstnamelastname@test.com
        f"{firstname[0]}{lastname}@{domain}", #flastname@test.com
        f"{firstname}{lastname[0]}@{domain}", #fistnamel@test.com

        f"{lastname}.{firstname}@{domain}", #lastname.firstname@test.com
        f"{lastname[0]}.{firstname}@{domain}", #l.firstname@test.com
        f"{lastname}.{firstname[0]}@{domain}", #lastname.f@test.com

        f"{lastname}-{firstname}@{domain}", #lastname-firstname@test.com
        f"{lastname[0]}-{firstname}@{domain}", #l-firstname@test.com
        f"{lastname}-{firstname[0]}@{domain}", #lastname-f@test.com

        f"{lastname}_{firstname}@{domain}", #lastname_firstname@test.com
        f"{lastname[0]}_{firstname}@{domain}", #l_firstname@test.com
        f"{lastname}_{firstname[0]}@{domain}", #lastname_f@test.com

        f"{lastname}{firstname}@{domain}", #lastnamefirstname@test.com
        f"{lastname[0]}{firstname}@{domain}", #lfirstname@test.com
        f"{lastname}{firstname[0]}@{domain}", #lastnamef@test.com

        f"{firstname}@{domain}", #firstname@test.com
        f"{lastname}@{domain}", #lastname@test.com

    # FIRST CHARACTER ONLY

        f"{firstname[0]}.{lastname[0]}@{domain}", #f.l@test.com
        f"{lastname[0]}.{firstname[0]}@{domain}", #l.f@test.com

        f"{firstname[0]}-{lastname[0]}@{domain}", #f-l@test.com
        f"{lastname[0]}-{firstname[0]}@{domain}", #l-f@test.com

        f"{firstname[0]}_{lastname[0]}@{domain}", #f_l@test.com
        f"{lastname[0]}_{firstname[0]}@{domain}", #l_f@test.com

        f"{firstname[0]}{lastname[0]}@{domain}", #fl@test.com
        f"{lastname[0]}{firstname[0]}@{domain}", #lf@test.com

        f"{firstname[0]}@{domain}", #f@test.com
        f"{lastname[0]}@{domain}", #l@test.com

    ]
	return email_variants